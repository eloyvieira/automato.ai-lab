from fine_tuning.dataset_builder import trading_decision_example, write_jsonl

examples = [
    trading_decision_example(
        'Classifique a posição somente como HOLD, EXIT ou REDUCE.',
        {'btc_regime':'LONG_WEAK','alt_regime':'LONG_STRONG','current_perc':1.4,'max_perc':1.9,'macd':'weakening'},
        {'decision':'HOLD','risk':'MEDIUM'}
    )
]

if __name__ == '__main__':
    print(write_jsonl(examples, 'fine_tuning/datasets/example.jsonl'))
