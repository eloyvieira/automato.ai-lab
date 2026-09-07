from fastapi import APIRouter
from app.api.schemas import ChatRequest, ChatResponse, AgentChatRequest, AgentChatResponse
from ai.orchestrator.service import AIOrchestrator

router = APIRouter()

@router.get('/health')
async def health():
    return {'ok': True}

@router.post('/chat', response_model=ChatResponse)
async def chat(payload: ChatRequest):
    """Fluxo legado/manual, preservado para comparação."""
    orchestrator = AIOrchestrator()
    return await orchestrator.ask(payload.message, payload.history)

@router.post('/agent/chat', response_model=AgentChatResponse)
async def agent_chat(payload: AgentChatRequest):
    """Novo fluxo LangChain + LangGraph com tools, RAG e memória por thread."""
    from agents.service import LangGraphAgentService
    agent = LangGraphAgentService()
    return await agent.ask(payload.message, payload.thread_id)

@router.get('/agent/info')
async def agent_info():
    return {
        'engine': 'langgraph',
        'framework': 'langchain',
        'legacy_endpoint': '/api/chat',
        'agent_endpoint': '/api/agent/chat',
        'features': ['tool-calling', 'rag-tool', 'thread-memory', 'provider-adapter', 'mcp-compatible-core-tools'],
    }
