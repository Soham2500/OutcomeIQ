"""Google Gemini provider adapter."""

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


class GeminiProvider:
    provider = "gemini"

    def run(self, prompt: str, model: str) -> ProviderResult:
        settings = get_settings()
        if not settings.GEMINI_API_KEY:
            raise AiProviderError("GEMINI_API_KEY is not configured.")

        try:
            from google import genai
        except ImportError as exc:
            raise AiProviderError(
                "google-genai package is not installed in the backend image."
            ) from exc

        started = perf_counter()
        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
        except Exception as exc:
            raise AiProviderError("Gemini request failed.") from exc

        latency_ms = int((perf_counter() - started) * 1000)
        usage = _get_attr_or_key(response, "usage_metadata", {}) or {}
        input_tokens = int(_get_attr_or_key(usage, "prompt_token_count", 0) or 0)
        output_tokens = int(
            _get_attr_or_key(usage, "candidates_token_count", 0) or 0
        )
        total_tokens = int(
            _get_attr_or_key(
                usage,
                "total_token_count",
                input_tokens + output_tokens,
            )
            or 0
        )
        raw_usage = {
            "prompt_token_count": input_tokens,
            "candidates_token_count": output_tokens,
            "total_token_count": total_tokens,
        }
        return ProviderResult(
            provider=self.provider,
            model=model,
            response_text=str(getattr(response, "text", "") or ""),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            raw_usage=raw_usage,
            latency_ms=latency_ms,
        )
