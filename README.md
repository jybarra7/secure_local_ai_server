Secure Local AI Inference Server with Private RAG Pipeline

# Overview
A local AI assistant running on a dedicated Apple Silicon server. Indexes and 
searches
personal documents using a private RAG pipeline. Accessible securely from a 
second
machine via Tailscale. Zero cloud exposure, zero third party data access.

# Architecture
- *Server*: MacBook Air M1 (headless) — runs Ollama + Gemma 3 4B + FastAPI
- *Client*: MacBook Air M5 — queries server via Tailscale private network
- *Network*: Tailscale encrypted mesh, no public internet exposure

# Stack
- Ollama — local LLM inference engine
- Gemma 3 4B — language model
- nomic-embed-text — embedding model
- LlamaIndex — RAG orchestration
- ChromaDB — local vector database
- FastAPI — REST API layer
- Tailscale — private encrypted network
- LuLu — outbound connection monitoring

# Threat Model
## What I'm protecting
- Personal documents: resume, job descriptions, capstone notes, study 
materials
- Home network integrity
- Server from unauthorized access

# Who can access
- Only me, from devices I control
- Only over Tailscale encrypted private network
- No open ports, no public endpoints

# Trust boundaries
- M1 server: Ollama and API bound to Tailscale IP only
- M5 client: queries via Tailscale only
- Public internet: no access whatsoever

# Threat & mitigations
|           Threat              |          Mitigation              |
|---                            |                               ---|
| Unauthorized network access | Tailscale only, no public ports |
| Exposed API endpoints | API key authentication on all endpoints |
| Prompt injection | Input validation layer |
| Unintended outbound connections | LuLu firewall monitoring |

# API Endpoints
- POST /query: query the RAG pipeline (requires API key)
- GET /health: health check

# Build Log
- Phase 0: Threat model documented
- Phase 1: Ollama installed, Gemma 3 4B running, locked to localhost
- Phase 2: RAG pipeline working, ChromaDB ingesting docs locally
- Phase 3: FastAPI secured, Tailscale two-node network live
- Phase 4: Documentation and GitHub
