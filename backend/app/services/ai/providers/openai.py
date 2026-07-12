"""OpenAI / ChatGPT provider adapter."""

from time import perf_counter
from typing import Any

from app.core.config import get_settings
from app.services.ai.providers.base import AiProviderError, ProviderResult


def _get_attr_or_key(source: Any, name: str, default: Any = None) -> Any:
    if source is None:
        return default
    if isinstance(source, dict):
        return source.get(name, default)
    return getattr(source, name, default)


def _response_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return str(output_text)
    choices = _get_attr_or_key(response, "choices", None)
    if choices:
        message = _get_attr_or_key(choices[0], "message", None)
        return str(_get_attr_or_key(message, "content", "") or "")
    return ""


def _usage_counts(response: Any) -> tuple[int, int, int, dict[str, int]]:
    usage = _get_attr_or_key(response, "usage", {}) or {}
    input_tokens = int(
        _get_attr_or_key(
            usage,
            "input_tokens",
            _get_attr_or_key(usage, "prompt_tokens", 0),
        )
        or 0
    )
    output_tokens = int(
        _get_attr_or_key(
            usage,
            "output_tokens",
            _get_attr_or_key(usage, "completion_tokens", 0),
        )
        or 0
    )
    total_tokens = int(
        _get_attr_or_key(
            usage,
            "total_tokens",
            input_tokens + output_tokens,
        )
        or 0
    )
    return (
        input_tokens,
        output_tokens,
        total_tokens,
        {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
        },
    )


class OpenAIProvider:
    provider = "openai"

    def run(self, prompt: str, model: str) -> ProviderResult:
        settings = get_settings()
        if not settings.OPENAI_API_KEY:
            raise AiProviderError("OPENAI_API_KEY is not configured.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise AiProviderError(
                "openai package is not installed in the backend image."
            ) from exc

        started = perf_counter()
        try:
            client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=settings.AI_PROVIDER_TIMEOUT_SECONDS,
            )
            if hasattr(client, "responses"):
                response = client.responses.create(model=model, input=prompt)
            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                )
        except Exception as exc:
            raise AiProviderError("OpenAI request failed.") from exc

        latency_ms = int((perf_counter() - started) * 1000)
        input_tokens, output_tokens, total_tokens, raw_usage = _usage_counts(response)
        return ProviderResult(
            provider=self.provider,
            model=model,
            response_text=_response_text(response),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            raw_usage=raw_usage,
            latency_ms=latency_ms,
        )
