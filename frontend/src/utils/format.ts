import type { DecimalValue } from "../types/dashboard";

export function toFiniteNumber(
  value: DecimalValue | null | undefined,
): number | null {
  if (value === null || value === undefined || value === "") {
    return null;
  }
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export function formatINR(value: DecimalValue | null | undefined): string {
  const amount = Number(value || 0);
  if (Math.abs(amount) > 0 && Math.abs(amount) < 0.01) {
    return `₹${amount.toFixed(4)}`;
  }
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function getINRCostWithFallback(
  costInr: DecimalValue | null | undefined,
  costUsd: DecimalValue | null | undefined,
): number {
  const parsedInr = toFiniteNumber(costInr);
  if (parsedInr !== null) {
    return parsedInr;
  }
  // Fallback conversion. Prefer backend cost_inr.
  return Number(costUsd || 0) * 83.5;
}

export function formatLegacyCostAsINR(value: DecimalValue | null | undefined): string {
  return formatINR(getINRCostWithFallback(null, value));
}

export function formatINRWithUsdFallback(
  costInr: DecimalValue | null | undefined,
  costUsd: DecimalValue | null | undefined,
): string {
  return formatINR(getINRCostWithFallback(costInr, costUsd));
}

export function formatPercent(
  value: DecimalValue | null | undefined,
): string {
  const parsed = toFiniteNumber(value);
  return parsed === null ? "—" : `${(parsed * 100).toFixed(1)}%`;
}

export function shortId(value: string | null | undefined): string {
  if (!value) {
    return "—";
  }
  return value.length <= 8 ? value : value.slice(0, 8);
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return "—";
  }
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString();
}
