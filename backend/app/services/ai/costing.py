"""AI token pricing helpers.

Provider prices change. Verify and update this map from official provider
pricing pages before relying on it for production billing or finance reports.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


MONEY_QUANTUM = Decimal("0.00000001")


@dataclass(frozen=True)
class AiCost:
    cost_usd: Decimal
    cost_inr: Decimal
    pricing_unknown: bool


@dataclass(frozen=True)
class PricingEntry:
    input_per_1m_usd: Decimal
    output_per_1m_usd: Decimal


PRICING_BY_PROVIDER_MODEL: dict[tuple[str, str], PricingEntry] = {
    ("gemini", "gemini-2.5-flash"): PricingEntry(
        input_per_1m_usd=Decimal("0.30"),
        output_per_1m_usd=Decimal("2.50"),
    ),
    ("gemini", "gemini-2.5-flash-lite"): PricingEntry(
        input_per_1m_usd=Decimal("0.10"),
        output_per_1m_usd=Decimal("0.40"),
    ),
    ("openai", "gpt-4o-mini"): PricingEntry(
        input_per_1m_usd=Decimal("0.15"),
        output_per_1m_usd=Decimal("0.60"),
    ),
    ("openai", "gpt-4.1-mini"): PricingEntry(
        input_per_1m_usd=Decimal("0.40"),
        output_per_1m_usd=Decimal("1.60"),
    ),
}


def _money(value: Decimal) -> Decimal:
    return value.quantize(MONEY_QUANTUM, rounding=ROUND_HALF_UP)


def calculate_ai_cost(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    usd_to_inr_rate: Decimal,
) -> AiCost:
    pricing = PRICING_BY_PROVIDER_MODEL.get((provider.lower(), model))
    if pricing is None:
        return AiCost(
            cost_usd=Decimal("0").quantize(MONEY_QUANTUM),
            cost_inr=Decimal("0").quantize(MONEY_QUANTUM),
            pricing_unknown=True,
        )

    input_cost = (
        Decimal(max(input_tokens, 0))
        / Decimal("1000000")
        * pricing.input_per_1m_usd
    )
    output_cost = (
        Decimal(max(output_tokens, 0))
        / Decimal("1000000")
        * pricing.output_per_1m_usd
    )
    cost_usd = _money(input_cost + output_cost)
    return AiCost(
        cost_usd=cost_usd,
        cost_inr=_money(cost_usd * usd_to_inr_rate),
        pricing_unknown=False,
    )
