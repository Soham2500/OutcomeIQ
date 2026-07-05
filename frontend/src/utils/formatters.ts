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

export function formatUsd(value: DecimalValue | null | undefined): string {
  const parsed = toFiniteNumber(value);
  if (parsed === null) {
    return "—";
  }
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: parsed < 0.01 ? 4 : 2,
    maximumFractionDigits: parsed < 0.01 ? 6 : 2,
  }).format(parsed);
}

export function formatPercentage(
  value: DecimalValue | null | undefined,
): string {
  const parsed = toFiniteNumber(value);
  return parsed === null ? "—" : `${(parsed * 100).toFixed(1)}%`;
}

export function formatDateTime(value: string | null | undefined): string {
  if (!value) {
    return "—";
  }
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "—" : date.toLocaleString();
}
