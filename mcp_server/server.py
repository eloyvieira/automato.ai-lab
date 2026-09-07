from mcp.server.fastmcp import FastMCP
from core.config import get_settings
from tools.registry import TOOLS, execute_tool

mcp = FastMCP(get_settings().mcp_server_name)

# Exposição explícita das tools. A lógica real continua em tools/.
@mcp.tool()
async def get_trades(start_date: str | None = None, end_date: str | None = None, conclusion: str | None = None, symbol: str | None = None, limit: int = 100):
    return await execute_tool('get_trades', locals())

@mcp.tool()
async def get_trade_by_id(order_id: int):
    return await execute_tool('get_trade_by_id', locals())

@mcp.tool()
async def get_open_positions(limit: int = 100):
    return await execute_tool('get_open_positions', locals())

@mcp.tool()
async def get_robot_stats(start_date: str, end_date: str | None = None):
    return await execute_tool('get_robot_stats', locals())

@mcp.tool()
async def get_btc_regime_history(start_date: str, end_date: str | None = None, limit: int = 500):
    return await execute_tool('get_btc_regime_history', locals())

@mcp.tool()
async def get_symbol_regime_history(symbol: str, start_date: str, end_date: str | None = None, limit: int = 500):
    return await execute_tool('get_symbol_regime_history', locals())

@mcp.tool()
async def get_ai_analysis(start_date: str | None = None, end_date: str | None = None, decision: str | None = None, order_id: int | None = None, limit: int = 100):
    return await execute_tool('get_ai_analysis', locals())

@mcp.tool()
async def get_current_btc_regime():
    return await execute_tool('get_current_btc_regime', {})

@mcp.tool()
async def get_current_symbol_regime(symbol: str):
    return await execute_tool('get_current_symbol_regime', locals())

@mcp.tool()
async def get_robot_status():
    return await execute_tool('get_robot_status', {})

@mcp.tool()
async def get_market_snapshot(symbol: str, timeframe: str = '15m'):
    return await execute_tool('get_market_snapshot', locals())

if __name__ == '__main__':
    mcp.run()
