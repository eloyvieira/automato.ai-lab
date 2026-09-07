# Changelog

## 2.0.0-lab
- Preserva `/api/chat` e `ai/orchestrator/` originais.
- Adiciona `/api/agent/chat` com LangChain + LangGraph.
- Adiciona adapters de modelo, Core Tools e RAG.
- Reutiliza as mesmas Core Tools já expostas pelo MCP Server.
- Adiciona memória por `thread_id` via LangGraph checkpointer.
- Adiciona factory de checkpointer e ponto de extensão para observabilidade.
- Mantém todos os SQLs como responsabilidade do usuário.
