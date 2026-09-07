# AI Lab

Laboratório modular de IA para integrar LLMs, ferramentas, MCP, RAG, memória, fine-tuning, LangChain e LangGraph.

## High-Level Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                          CLIENTS                             │
│                                                              │
│     Web App       Voice Interface       Robot / External App │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
                    ┌───────────────────┐
                    │      FastAPI      │
                    │    API Gateway    │
                    └─────────┬─────────┘
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
    ┌─────────────────────┐       ┌─────────────────────┐
    │    BASIC AI FLOW    │       │   AGENTIC AI FLOW  │
    │                     │       │                     │
    │   AI Orchestrator   │       │     LangChain      │
    │    Original Flow    │       │    + LangGraph     │
    └──────────┬──────────┘       └──────────┬──────────┘
               │                             │
               └──────────────┬──────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │     LLM PROVIDER       │
                  │        LAYER           │
                  ├────────────────────────┤
                  │ OpenAI                 │
                  │ Gemini                 │
                  │ Local LLM              │
                  │ Future Providers       │
                  └────────────┬───────────┘
                               │
                               ▼
                    ┌────────────────────┐
                    │        LLM         │
                    └─────────┬──────────┘
                              │
                   Tool / Retrieval Calls
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
   ┌──────────────────────┐        ┌──────────────────────┐
   │      CORE TOOLS      │        │         RAG          │
   ├──────────────────────┤        │      RETRIEVAL       │
   │ MySQL Tools          │        ├──────────────────────┤
   │ Redis Tools          │        │ SQL Retriever        │
   │ Trading Tools        │        │ Vector Retriever     │
   │ Market Tools         │        └──────────┬───────────┘
   │ Robot Tools          │                   │
   │ System Tools         │             ┌─────┴─────┐
   └──────────┬───────────┘             ▼           ▼
              │                       MySQL      Vector DB
              │                                  Future
              ▼
     ┌────────────────────┐
     │     MCP SERVER     │
     │ exposes Core Tools │
     └─────────┬──────────┘
               │
               ▼
        External Agents
```

## Rodar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Acesse:

```text
http://localhost:8010/
```

Endpoints principais:

```text
POST /api/chat
POST /api/agent/chat
```

## Provider

Configure no `.env`:

```env
LLM_PROVIDER=openai
```

A camada de provider permite adicionar Gemini ou modelos locais sem alterar Tools, RAG ou MCP.

## SQL

Os SQLs devem ser implementados em:

```text
tools/mysql/
rag/sql_retriever.py
ai/memory/
ai/orchestrator/
```

Nenhum SQL foi incluído propositalmente.

## MCP

```bash
python -m mcp_server.server
```

O MCP reutiliza as mesmas Core Tools usadas pelo fluxo tradicional e pelo LangGraph Agent.

## Fine-Tuning

O projeto possui pipeline separado para criação de datasets e jobs de fine-tuning, sem acoplar o treinamento ao runtime da aplicação.
