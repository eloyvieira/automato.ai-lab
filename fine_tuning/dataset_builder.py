import json
from pathlib import Path
from typing import Iterable

REQUIRED_ROLES = {'system', 'user', 'assistant'}

def validate_example(example: dict) -> None:
    messages = example.get('messages')
    if not isinstance(messages, list) or len(messages) < 2:
        raise ValueError('Cada exemplo precisa conter messages.')
    for message in messages:
        if message.get('role') not in REQUIRED_ROLES:
            raise ValueError(f"Role inválido: {message.get('role')}")
        if not isinstance(message.get('content'), str) or not message['content'].strip():
            raise ValueError('content precisa ser texto não vazio.')

def write_jsonl(examples: Iterable[dict], output_path: str) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open('w', encoding='utf-8') as f:
        for example in examples:
            validate_example(example)
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
            count += 1
    if count == 0: raise ValueError('Dataset vazio.')
    return str(path)

def trading_decision_example(system_prompt: str, context: dict, expected_answer: dict) -> dict:
    return {
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': json.dumps(context, ensure_ascii=False)},
            {'role': 'assistant', 'content': json.dumps(expected_answer, ensure_ascii=False)},
        ]
    }
