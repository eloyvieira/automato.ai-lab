import asyncio
from ai.orchestrator.service import AIOrchestrator

async def process(message: str):
    return await AIOrchestrator().ask(message)

if __name__ == '__main__':
    print(asyncio.run(process('Qual é o status atual do robô?')))
