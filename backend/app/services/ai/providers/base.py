"""Shared contracts for AI provider adapters."""

from dataclasses import dataclass, field
from typing import Any, Protocol


class AiProviderError(RuntimeError):
    """Safe provider error that can be returned to authenticated users."""


@dataclass(frozen=True)
class ProviderResult:
    provider: str
    model: str
    response_text: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    raw_usage: dict[str, Any] = field(default_factory=dict)
    latency_ms: int = 0


class AiProvider(Protocol):
    provider: str

    def run(self, prompt: str, model: str) -> ProviderResult:
        """Run a prompt against a configured backend provider."""
