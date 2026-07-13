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
  const parsed = toFiniteNumber(value);
  if (parsed === null) {
    return "—";
  }
  if (parsed !== 0 && Math.abs(parsed) < 0.00005) {
    return parsed > 0 ? "<₹0.0001" : ">-₹0.0001";
  }
  const tiny = Math.abs(parsed) < 0.01;
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    minimumFractionDigits: tiny ? 4 : 2,
    maximumFractionDigits: tiny ? 4 : 2,
  }).format(parsed);
}

export function formatLegacyCostAsINR(value: DecimalValue | null | undefined): string {
  const parsed = toFiniteNumber(value);
  // Fallback INR conversion. Prefer backend cost_inr when available.
  return parsed === null ? "—" : formatINR(parsed * 83.5);
}

export function formatINRWithUsdFallback(
  costInr: DecimalValue | null | undefined,
  costUsd: DecimalValue | null | undefined,
): string {
  const parsedInr = toFiniteNumber(costInr);
  if (parsedInr !== null) {
    return formatINR(parsedInr);
  }
  return formatLegacyCostAsINR(costUsd);
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
