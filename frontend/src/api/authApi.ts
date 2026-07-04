import { apiClient } from "./client";
import type {
  CurrentUser,
  LoginRequest,
  RegisterRequest,
  TokenResponse,
} from "../types/auth";

export async function login(request: LoginRequest): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>("/auth/login", request);
  return response.data;
}

export async function register(request: RegisterRequest): Promise<CurrentUser> {
  const response = await apiClient.post<CurrentUser>("/auth/register", request);
  return response.data;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await apiClient.get<CurrentUser>("/auth/me");
  return response.data;
}
