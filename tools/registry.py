import inspect
from typing import Any
from tools.base import ToolDefinition
from tools.mysql.trades import get_trades, get_trade_by_id, get_open_positions
from tools.mysql.stats import get_robot_stats
from tools.mysql.regimes import get_btc_regime_history, get_symbol_regime_history
from tools.mysql.analysis import get_ai_analysis
from tools.redis.market import get_current_btc_regime, get_current_symbol_regime
from tools.trading.robot import get_robot_status, get_market_snapshot

OBJECT = {'type': 'object', 'additionalProperties': False}

def schema(properties: dict, required: list[str] | None = None) -> dict:
    return {**OBJECT, 'properties': properties, 'required': required or []}

TOOLS: dict[str, ToolDefinition] = {
    'get_trades': ToolDefinition('get_trades','Busca operações no histórico.',schema({
        'start_date': {'type':['string','null']}, 'end_date': {'type':['string','null']}, 'conclusion': {'type':['string','null']},
        'symbol': {'type':['string','null']}, 'limit': {'type':'integer','minimum':1,'maximum':500}
    },['start_date','end_date','conclusion','symbol','limit']),get_trades),
    'get_trade_by_id': ToolDefinition('get_trade_by_id','Busca uma operação pelo ID.',schema({'order_id':{'type':'integer'}},['order_id']),get_trade_by_id),
    'get_open_positions': ToolDefinition('get_open_positions','Lista posições abertas.',schema({'limit':{'type':'integer','minimum':1,'maximum':500}},['limit']),get_open_positions),
    'get_robot_stats': ToolDefinition('get_robot_stats','Busca estatísticas agregadas do robô.',schema({'start_date':{'type':'string'},'end_date':{'type':['string','null']}},['start_date','end_date']),get_robot_stats),
    'get_btc_regime_history': ToolDefinition('get_btc_regime_history','Busca histórico de regimes do Bitcoin.',schema({'start_date':{'type':'string'},'end_date':{'type':['string','null']},'limit':{'type':'integer','minimum':1,'maximum':2000}},['start_date','end_date','limit']),get_btc_regime_history),
    'get_symbol_regime_history': ToolDefinition('get_symbol_regime_history','Busca histórico de regimes de uma moeda.',schema({'symbol':{'type':'string'},'start_date':{'type':'string'},'end_date':{'type':['string','null']},'limit':{'type':'integer','minimum':1,'maximum':2000}},['symbol','start_date','end_date','limit']),get_symbol_regime_history),
    'get_ai_analysis': ToolDefinition('get_ai_analysis','Busca análises anteriores da IA.',schema({'start_date':{'type':['string','null']},'end_date':{'type':['string','null']},'decision':{'type':['string','null']},'order_id':{'type':['integer','null']},'limit':{'type':'integer','minimum':1,'maximum':500}},['start_date','end_date','decision','order_id','limit']),get_ai_analysis),
    'get_current_btc_regime': ToolDefinition('get_current_btc_regime','Obtém o regime atual do BTC no Redis.',schema({}),get_current_btc_regime),
    'get_current_symbol_regime': ToolDefinition('get_current_symbol_regime','Obtém o regime atual da moeda no Redis.',schema({'symbol':{'type':'string'}},['symbol']),get_current_symbol_regime),
    'get_robot_status': ToolDefinition('get_robot_status','Obtém status operacional do robô.',schema({}),get_robot_status),
    'get_market_snapshot': ToolDefinition('get_market_snapshot','Obtém snapshot atual de indicadores de uma moeda.',schema({'symbol':{'type':'string'},'timeframe':{'type':'string'}},['symbol','timeframe']),get_market_snapshot),
}

def get_openai_tools() -> list[dict[str, Any]]:
    return [tool.openai_schema() for tool in TOOLS.values()]

async def execute_tool(name: str, arguments: dict[str, Any]) -> Any:
    if name not in TOOLS: raise ValueError(f'Tool desconhecida: {name}')
    handler = TOOLS[name].handler
    result = handler(**arguments)
    return await result if inspect.isawaitable(result) else result
