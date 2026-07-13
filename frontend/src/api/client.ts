import axios, { AxiosError } from "axios";

export const TOKEN_KEY = "outcomeiq_access_token";

const LOCAL_API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const PRODUCTION_API_BASE_URL = "https://api.outcomedata.in/api/v1";
const INSECURE_PRODUCTION_URL_PATTERN = /^http:\/\/(?!localhost(?::\d+)?(?:\/|$)|127\.0\.0\.1(?::\d+)?(?:\/|$))/i;

function normalizeApiBaseUrl(rawBaseUrl?: string): string {
  const candidate = (rawBaseUrl ?? "").trim().replace(/\/$/, "");

  if (!candidate) {
    return typeof window !== "undefined" && window.location.protocol === "https:"
      ? PRODUCTION_API_BASE_URL
      : LOCAL_API_BASE_URL;
  }

  if (
    typeof window !== "undefined" &&
    window.location.protocol === "https:" &&
    INSECURE_PRODUCTION_URL_PATTERN.test(candidate)
  ) {
    return PRODUCTION_API_BASE_URL;
  }

  return candidate;
}

const configuredBaseUrl = normalizeApiBaseUrl(import.meta.env.VITE_API_BASE_URL);

if (import.meta.env.DEV) {
  console.info("[OutcomeIQ API] Base URL:", configuredBaseUrl);
}

export const apiClient = axios.create({
  baseURL: configuredBaseUrl,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
  timeout: 20_000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const status = error.response?.status;
    const detail = (error.response?.data as ApiErrorPayload | undefined)?.detail;
    const message =
      typeof detail === "string"
        ? detail
        : (error.response?.data as ApiErrorPayload | undefined)?.message;
    console.warn("[OutcomeIQ API] Request failed", {
      method: error.config?.method,
      url: error.config?.url,
      status,
      message: message ?? error.message,
    });
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      if (
        typeof window !== "undefined" &&
        !window.location.pathname.startsWith("/login") &&
        !window.location.pathname.startsWith("/register")
      ) {
        window.location.assign("/login");
      }
    }
    return Promise.reject(error);
  },
);

interface ApiErrorPayload {
  detail?: string | Array<{ msg?: string }>;
  message?: string;
}

export function getApiErrorMessage(
  error: unknown,
  fallback = "The request could not be completed.",
): string {
  if (!axios.isAxiosError<ApiErrorPayload>(error)) {
    return error instanceof Error ? error.message : fallback;
  }

  const detail = error.response?.data?.detail;
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail)) {
    const messages = detail.map((item) => item.msg).filter(Boolean);
    if (messages.length > 0) {
      return messages.join(" ");
    }
  }
  return error.response?.data?.message ?? fallback;
}

export function isApiStatus(error: unknown, status: number): boolean {
  return axios.isAxiosError(error) && error.response?.status === status;
}

export function isApiNetworkError(error: unknown): boolean {
  return axios.isAxiosError(error) && error.response === undefined;
}

export function getApiBaseUrl(): string {
  return configuredBaseUrl;
}
