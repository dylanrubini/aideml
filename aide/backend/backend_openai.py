"""Backend for OpenAI API."""

import json
import logging
import time

import openai
from funcy import notnone, once, select_values

from .openai_api_pricing import OAI_Pricing
from .utils import (
    FunctionSpec,
    OutputType,
    backoff_create,
    opt_messages_to_list,
)

logger = logging.getLogger("aide")

_client: openai.OpenAI = None  # type: ignore
oai_spending = None  # type: ignore

OPENAI_TIMEOUT_EXCEPTIONS = (
    openai.RateLimitError,
    openai.APIConnectionError,
    openai.APITimeoutError,
    openai.InternalServerError,
)


@once
def _setup_openai_client(model, per_run_token_limit):
    global _client, oai_spending
    oai_spending = OAI_Pricing(model, per_run_token_limit)
    _client = openai.OpenAI(max_retries=0)


def query(
    per_run_token_limit: int,
    system_message: str | None,
    user_message: str | None,
    func_spec: FunctionSpec | None = None,
    **model_kwargs,
) -> tuple[OutputType, float, int, int, dict]:
    """
    Query the OpenAI API, optionally with function calling.
    If the model doesn't support function calling, gracefully degrade to text generation.
    """
    global oai_spending

    _setup_openai_client(model_kwargs["model"], per_run_token_limit)
    filtered_kwargs: dict = select_values(notnone, model_kwargs)

    # Convert system/user messages to the format required by the client
    messages = opt_messages_to_list(system_message, user_message)

    # If function calling is requested, attach the function spec
    if func_spec is not None:
        filtered_kwargs["tools"] = [func_spec.as_openai_tool_dict]
        filtered_kwargs["tool_choice"] = func_spec.openai_tool_choice_dict

    if model_kwargs["model"] == "o3-mini":
        filtered_kwargs["reasoning_effort"] = "high"
        del filtered_kwargs["temperature"]  # o3-mini does not support this

    completion = None
    t0 = time.time()

    allowed_models = ["gpt-4o-mini", "qwen2.5"]  # "o3-mini"
    if model_kwargs["model"] not in allowed_models:
        raise NotImplementedError(
            f"Only the models {allowed_models} are currently allowed"
        )

    # Attempt the API call
    try:
        completion = backoff_create(
            _client.chat.completions.create,
            OPENAI_TIMEOUT_EXCEPTIONS,
            messages=messages,
            **filtered_kwargs,
        )
    except openai.BadRequestError as e:
        # Check whether the error indicates that function calling is not supported
        if "function calling" in str(e).lower() or "tools" in str(e).lower():
            logger.warning(
                "Function calling was attempted but is not supported by this model. "
                "Falling back to plain text generation."
            )
            # Remove function-calling parameters and retry
            filtered_kwargs.pop("tools", None)
            filtered_kwargs.pop("tool_choice", None)

            # Retry without function calling
            completion = backoff_create(
                _client.chat.completions.create,
                OPENAI_TIMEOUT_EXCEPTIONS,
                messages=messages,
                **filtered_kwargs,
            )
        else:
            # If it's some other error, re-raise
            raise

    req_time = time.time() - t0
    choice = completion.choices[0]

    # Decide how to parse the response
    if func_spec is None or "tools" not in filtered_kwargs:
        # No function calling was ultimately used
        output = choice.message.content
    else:
        # Attempt to extract tool calls
        tool_calls = getattr(choice.message, "tool_calls", None)
        if not tool_calls:
            logger.warning(
                "No function call was used despite function spec. Fallback to text.\n"
                f"Message content: {choice.message.content}"
            )
            output = choice.message.content
        else:
            first_call = tool_calls[0]
            # Optional: verify that the function name matches
            if first_call.function.name != func_spec.name:
                logger.warning(
                    f"Function name mismatch: expected {func_spec.name}, "
                    f"got {first_call.function.name}. Fallback to text."
                )
                output = choice.message.content
            else:
                try:
                    output = json.loads(first_call.function.arguments)
                except json.JSONDecodeError as ex:
                    logger.error(
                        "Error decoding function arguments:\n"
                        f"{first_call.function.arguments}"
                    )
                    raise ex

    in_tokens = completion.usage.prompt_tokens
    out_tokens = completion.usage.completion_tokens
    oai_spending.update(in_tokens, out_tokens)
    oai_spending.print()

    info = {
        "system_fingerprint": completion.system_fingerprint,
        "model": completion.model,
        "created": completion.created,
    }

    return output, req_time, in_tokens, out_tokens, info
