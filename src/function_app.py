# =============================================================================
#
# This application demonstrates a modern AI-powered code snippet manager built with:
#
# 1. Azure Functions - Serverless compute that runs your code in the cloud
#    - HTTP triggers - Standard RESTful API endpoints accessible over HTTP
#    - MCP triggers - Model Context Protocol for AI agent integration (e.g., GitHub Copilot)
#
# 2. Azure Cosmos DB - NoSQL database with vector search capability
#    - Stores code snippets and their vector embeddings
#    - Enables semantic search through vector similarity
#
# 3. Azure OpenAI - Provides AI models and embeddings
#    - Generates vector embeddings from code snippets
#    - These embeddings capture the semantic meaning of the code
#
# 4. Azure AI Agents - Specialized AI agents for code analysis
#    - For generating documentation and style guides from snippets
#
# The application provides two parallel interfaces for the same functionality:
# - HTTP endpoints for traditional API access
# - MCP tools for AI assistant integration

import json
import logging
import azure.functions as func
import os

from azure.storage.blob.aio import BlobServiceClient

# Lazy import placeholder for cosmos operations (import inside function to avoid startup failure when env vars missing)
try:
    from data import cosmos_ops  # type: ignore
except Exception:
    cosmos_ops = None  # Will handle inside health check

app = func.FunctionApp()

# Register blueprints with enhanced error handling to prevent startup issues

# Core snippy functionality
try:
    from functions import bp_snippy
    app.register_blueprint(bp_snippy.bp)
    logging.info("✅ Snippy blueprint registered successfully")
except ImportError as e:
    logging.error(f"❌ Import error for Snippy blueprint: {e}")
except Exception as e:
    logging.error(f"❌ Snippy blueprint registration failed: {e}")

# Query functionality  
try:
    from routes import query
    app.register_blueprint(query.bp)
    logging.info("✅ Query blueprint registered successfully")
except ImportError as e:
    logging.error(f"❌ Import error for Query blueprint: {e}")
except Exception as e:
    logging.error(f"❌ Query blueprint registration failed: {e}")

# Embeddings functionality - now enabled for Level 2
try:
    from functions import bp_embeddings
    app.register_blueprint(bp_embeddings.bp)
    logging.info("✅ Embeddings blueprint registered successfully")
except ImportError as e:
    logging.error(f"❌ Import error for Embeddings blueprint: {e}")
except Exception as e:
    logging.error(f"❌ Embeddings blueprint registration failed: {e}")

# Ingestion functionality - blob trigger for Level 4
try:
    from functions import bp_ingestion
    app.register_blueprint(bp_ingestion.bp)
    logging.info("✅ Ingestion blueprint registered successfully")
except ImportError as e:
    logging.error(f"❌ Import error for Ingestion blueprint: {e}")
except Exception as e:
    logging.error(f"❌ Ingestion blueprint registration failed: {e}")

# Multi-agent functionality
try:
    from functions import bp_multi_agent
    app.register_blueprint(bp_multi_agent.bp)
    logging.info("✅ Multi-agent blueprint registered successfully")
except ImportError as e:
    logging.error(f"❌ Import error for Multi-agent blueprint: {e}")
except Exception as e:
    logging.error(f"❌ Multi-agent blueprint registration failed: {e}")


# =============================================================================
# HEALTH CHECK FUNCTIONALITY
# =============================================================================

# HTTP endpoint for health check
@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
async def http_health_check(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        JSON response with status "ok" and 200 status code
    """
    try:
        logging.info("Health check endpoint called")
        return func.HttpResponse(
            body=json.dumps({"status": "ok"}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in health check: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"status": "error", "message": str(e)}),
            mimetype="application/json",
            status_code=500
        )


# HTTP endpoint for health check
@app.route(route="health_extended", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
async def http_health_check_extended(req: func.HttpRequest) -> func.HttpResponse:
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        JSON response with status "ok" and 200 status code
    """
    # Storage account verification
    storage_status: str = "ok"
    cosmos_status: str = "skipped"
    try:
        storage_conn_str = os.environ["AzureWebJobsStorage"]
        ingestion_container = os.environ["INGESTION_CONTAINER"]
        blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)
        container_client = blob_service_client.get_container_client(ingestion_container)
        # Try listing blobs to verify access (limit to first)
        async for _ in container_client.list_blobs(results_per_page=1):  # type: ignore[arg-type]
            break
        logging.info(
            f"Storage account and container '{ingestion_container}' are accessible"
        )
    except Exception as e:
        storage_status = f"error: {e}"
        logging.error(f"Storage health check failed: {e}")
        return func.HttpResponse(
            body=json.dumps(
                {"status": "error", "storage": storage_status, "cosmos": cosmos_status}
            ),
            mimetype="application/json",
            status_code=500,
        )

    # Cosmos DB verification (only if module imported successfully)
    if cosmos_ops is not None:
        try:
            # Get container (creates if not exists) and run a very lightweight query
            container = await cosmos_ops.get_container()  # type: ignore[attr-defined]
            query_iter = container.query_items(
                query=(
                    "SELECT TOP 1 c.id FROM c WHERE c.type = 'code-snippet'"
                )
            )
            # Consume at most one item
            async for _ in query_iter:
                break
            cosmos_status = "ok"
            logging.info("Cosmos DB is accessible and query executed")
        except Exception as e:
            cosmos_status = f"error: {e}"
            logging.error(f"Cosmos DB health check failed: {e}")
            return func.HttpResponse(
                body=json.dumps(
                    {
                        "status": "error",
                        "storage": storage_status,
                        "cosmos": cosmos_status,
                    }
                ),
                mimetype="application/json",
                status_code=500,
            )
    else:
        cosmos_status = "module-import-failed"
        logging.warning(
            "cosmos_ops module not available; skipping Cosmos DB health check"
        )

    logging.info("Extended Health check endpoint called")
    return func.HttpResponse(
        body=json.dumps(
            {
                "status": "OK",
                "storage": storage_status,
                "cosmos": cosmos_status,
            }
        ),
        mimetype="application/json",
        status_code=200,
    )