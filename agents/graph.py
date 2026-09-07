from functools import lru_cache
from typing import Any
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from agents.state import AgentState
from agents.checkpoint import get_checkpointer
from ai.prompts.system import SYSTEM_PROMPT
from langchain_adapters.model import get_langchain_model
from langchain_adapters.retriever import get_rag_tool
from langchain_adapters.tools import get_langchain_tools


@lru_cache
def get_agent_graph() -> Any:
    """Grafo agentic paralelo ao AIOrchestrator legado.

    Fluxo: model -> tools/RAG -> model até haver resposta final.
    InMemorySaver é adequado ao lab; em produção troque por checkpointer persistente.
    """
    tools = [*get_langchain_tools(), get_rag_tool()]
    model = get_langchain_model().bind_tools(tools)

    async def model_node(state: AgentState):
        messages = state['messages']
        if not messages or getattr(messages[0], 'type', None) != 'system':
            from langchain_core.messages import SystemMessage
            messages = [SystemMessage(content=SYSTEM_PROMPT), *messages]
        response = await model.ainvoke(messages)
        return {'messages': [response]}

    graph = StateGraph(AgentState)
    graph.add_node('model', model_node)
    graph.add_node('tools', ToolNode(tools, handle_tool_errors=True))
    graph.add_edge(START, 'model')
    graph.add_conditional_edges('model', tools_condition, {'tools': 'tools', END: END})
    graph.add_edge('tools', 'model')
    return graph.compile(checkpointer=get_checkpointer())
