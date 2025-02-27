import json
import os
from datetime import datetime
from math import ceil
from pathlib import Path

MAX_DAY_SPENDING = 10.0  # dollars


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


class OAI_Pricing:

    def __init__(self, model, per_run_token_limit):

        self.model = model
        self.per_run_token_limit = per_run_token_limit
        self.last_modified_date = None
        self.token_spending_file = Path("./backend/spent_tokens.json")
        self.dollars_now = None
        self.tokens_now = None

        if not self.token_spending_file.exists():

            self.data = {
                "dollars_per_run": 0.0,
                "dollars_today": 0.0,
                "dollars_forever": 0.0,
                "tokens_per_run": 0,
                "tokens_today": 0,
                "tokens_forever": 0,
            }

            with open(self.token_spending_file, "w") as fh:
                json.dump(self.data, fh, indent=4)

        else:

            with open(self.token_spending_file, "r") as fh:
                self.data = json.load(fh)

            self.dollars_today = self.data["dollars_today"]
            self.dollars_forever = self.data["dollars_forever"]
            self.tokens_today = self.data["tokens_today"]
            self.tokens_forever = self.data["tokens_forever"]

            # reset per run quantities
            self.data["dollars_per_run"] = 0.0
            self.data["tokens_per_run"] = 0

        self.last_modified_date = datetime.fromtimestamp(
            os.path.getmtime(self.token_spending_file)
        ).date()

    def update(self, in_tokens: int, out_tokens: int) -> None:

        if self.model != "qwen2.5":

            self.tokens_now = in_tokens + out_tokens
            self.dollars_now = calculate_pricing(
                self.model, in_tokens, out_tokens
            )

            current_date = datetime.today().date()

            self.data["dollars_per_run"] += self.dollars_now
            self.data["dollars_forever"] += self.dollars_now
            self.data["tokens_per_run"] += self.tokens_now
            self.data["tokens_forever"] += self.tokens_now

            if current_date > self.last_modified_date:

                self.data["tokens_today"] = 0
                self.data["dollars_today"] = 0.0

            self.data["tokens_today"] += self.tokens_now
            self.data["dollars_today"] += self.dollars_now

            with open(self.token_spending_file, "w") as fh:
                json.dump(self.data, fh, indent=4)

    def print(self):

        if self.model != "qwen2.5":

            print("\n-------------------------------------")
            print(f"Spent now = ${self.dollars_now}")
            print(f"Spent this run = ${self.data['dollars_per_run']}")
            print(f"Spent today = ${self.data['dollars_today']}")
            print(f"Spent overall = ${self.data['dollars_forever']}")

            print(f"Total tokens now = {self.tokens_now}")
            print(f"Total tokens this run = {self.data['tokens_per_run']}")
            print(f"Total tokens today = {self.data['tokens_today']}")
            print(f"Total tokens overall = {self.data['tokens_forever']}")
            print("-------------------------------------\n")

            if self.tokens_now > self.per_run_token_limit:
                raise ValueError(
                    f"Exceeded token limit of {self.per_run_token_limit}"
                )

            if self.data["dollars_today"] > MAX_DAY_SPENDING:
                raise ValueError(
                    f"Exceeded max. day spending limit {MAX_DAY_SPENDING}"
                )
