from math import ceil

# price in dollars per 1000 tokens, WARNING: these are subject to change
model_price_map = {
    # OpenAI o1-preview
    "o1-input": 0.015,
    "o1-output": 0.060,
    # OpenAI o1-mini
    "o1-mini-input": 0.0011,
    "o1-mini-output": 0.0044,
    # OpenAI o3-mini
    "o3-mini-input": 0.0011,
    "o3-mini-output": 0.0044,
    # GPT-4o mini
    "gpt-4o-mini-input": 0.000150,
    "gpt-4o-mini-output": 0.000600,
    # GPT-4o
    "gpt-4o-input": 0.0025,
    "gpt-4o-output": 0.0100,
}
allowed_models = ["o1", "o1-mini", "gpt-4o-mini", "gpt-4o", "o3-mini"]


def calculate_pricing(model, token_input=0, token_output=0):

    if token_input == 0:
        return 0.0

    elif model in allowed_models:

        token_price = model_price_map.get(model + "-input")
        input_cost = (token_input / 1000) * token_price
        token_price = model_price_map.get(model + "-output")
        output_cost = (token_output / 1000) * token_price

        return input_cost + output_cost

    else:
        raise ValueError(f"Unknown model = {model}")
