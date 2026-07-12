export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest extends LoginRequest {
  full_name: string;
}

export type RegisterOtpRequest = RegisterRequest;

export interface VerifyRegistrationOtpRequest {
  email: string;
  otp: string;
}

export interface MessageResponse {
  message: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface CurrentUser {
  id: string;
  email: string;
  full_name: string | null;
  status: string;
}
