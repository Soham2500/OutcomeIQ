import { apiClient } from "./client";
import type {
  CurrentUser,
  LoginRequest,
  MessageResponse,
  RegisterOtpRequest,
  RegisterRequest,
  TokenResponse,
  VerifyRegistrationOtpRequest,
} from "../types/auth";

export async function login(request: LoginRequest): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>("/auth/login", request);
  return response.data;
}

export async function register(request: RegisterRequest): Promise<MessageResponse> {
  const response = await apiClient.post<MessageResponse>("/auth/register", request);
  return response.data;
}

export async function requestRegistrationOtp(
  request: RegisterOtpRequest,
): Promise<MessageResponse> {
  const response = await apiClient.post<MessageResponse>(
    "/auth/register/request-otp",
    request,
  );
  return response.data;
}

export async function verifyRegistrationOtp(
  request: VerifyRegistrationOtpRequest,
): Promise<CurrentUser> {
  const response = await apiClient.post<CurrentUser>(
    "/auth/register/verify-otp",
    request,
  );
  return response.data;
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const response = await apiClient.get<CurrentUser>("/auth/me");
  return response.data;
}
