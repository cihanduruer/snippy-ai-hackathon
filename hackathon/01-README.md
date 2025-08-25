# 🎯 Snippy AI Hackathon

Build an enterprise-grade AI-powered knowledge assistant using Azure Functions, Cosmos DB vector search, Azure OpenAI, and Zero Trust security.

### 🎯 Format
- **Duration**: 6 hours total
- **Teams**: 5/6 people per team
- **Tech Stack**: Azure Functions (Python 3.11), Cosmos DB, Azure OpenAI, Durable Functions

### 🏆 Levels Overview

#### Core Foundation
| Level | Focus | Key Deliverable |
|-------|--------|-----------------|
| **Level 1** | Foundation API + Persistence | CRUD operations, metadata storage |
| **Level 2** | Durable Orchestration | Fan-out embeddings, parallel processing |
| **Level 3** | Vector Search + Q&A | Semantic search, RAG with citations |
| **Level 4** | MCP Tool Integration | GitHub Copilot integration via MCP |

#### Advanced Enterprise
| Level | Focus | Key Deliverable |
|-------|--------|-----------------|
| **Level 5** | Event-driven + Observability | Auto-ingestion, monitoring, resilience |
| **Level 6** | Multi-Agent Orchestration | AI agents collaborating on complex tasks |
| **Level 7** | Zero Trust Security | Private endpoints, network isolation |

## 🎯 Winning Strategy

### ✅ Teams Aiming for Completion
1. **Focus on Levels 1-6 first**
2. **Attempt Level 7** if time permits
3. **Prioritize solid implementation** over feature breadth

### 🚀 Advanced Teams
1. **Split effort** between core (Levels 1-5) and advanced (Levels 6-7)
2. **Ensure integration** between all components
3. **Focus on architecture** and scalability

### 🎖️ Minimum Viable Product
Complete **Levels 1-6** for a fully functional AI knowledge assistant with:
- Code Snippet ingestion and storage
- AI-powered semantic search
- Question answering with citations
- GitHub Copilot integration
- Automated processing and monitoring
- Multi-agent AI workflows

## 📋 Technical Requirements

- **Azure subscription** use your respective Microsoft Non-Production (fdpo.onmicrosoft.com) subscription.
- **Python 3.11** with Azure Functions v2 blueprint model.
- **Durable orchestrators**: `def` (sync) with `yield` + `context.task_all(...)`.
- **Activity functions**: `async def` returning JSON-serializable data.
- **Cloud-first deployment**: Use `azd up` for all development and testing.
- **No local development**: All testing against deployed Azure resources.
- **Security**: No secrets in code, use environment variables and Managed Identity.

## 🚀 Quick Start

**👉 [Read the complete Getting Started Guide](./02-GETTING-STARTED.md)**

**Good luck, and happy hacking!** 🚀
