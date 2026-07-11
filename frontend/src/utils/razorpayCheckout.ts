import type { CheckoutResponse } from "../api/billingApi";

declare global {
  interface Window {
    Razorpay?: new (options: Record<string, unknown>) => {
      open: () => void;
    };
  }
}

const RAZORPAY_SCRIPT_URL = "https://checkout.razorpay.com/v1/checkout.js";

export function loadRazorpayScript(): Promise<boolean> {
  return new Promise((resolve) => {
    if (window.Razorpay) {
      resolve(true);
      return;
    }
    const existing = document.querySelector<HTMLScriptElement>(
      `script[src="${RAZORPAY_SCRIPT_URL}"]`,
    );
    if (existing) {
      existing.addEventListener("load", () => resolve(true), { once: true });
      existing.addEventListener("error", () => resolve(false), { once: true });
      return;
    }
    const script = document.createElement("script");
    script.src = RAZORPAY_SCRIPT_URL;
    script.async = true;
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
}

export async function openRazorpayCheckout(
  checkoutPayload: CheckoutResponse,
  onSuccess: (message: string) => void,
  onFailure: (message: string) => void,
) {
  if (
    checkoutPayload.checkout_type !== "razorpay_subscription" ||
    !checkoutPayload.key_id ||
    !checkoutPayload.subscription_id
  ) {
    onFailure("Razorpay is not configured on backend. Use local test activation.");
    return;
  }

  const loaded = await loadRazorpayScript();
  if (!loaded || !window.Razorpay) {
    onFailure("Could not load Razorpay Checkout script. Use local test activation.");
    return;
  }

  const checkout = new window.Razorpay({
    key: checkoutPayload.key_id,
    subscription_id: checkoutPayload.subscription_id,
    name: checkoutPayload.name ?? "OutcomeIQ",
    description:
      checkoutPayload.description ??
      "OutcomeIQ Razorpay test-mode subscription checkout.",
    prefill:
      checkoutPayload.prefill ??
      {
        email: checkoutPayload.prefill_email,
        name: checkoutPayload.prefill_name,
      },
    theme: {
      color: "#2563eb",
    },
    handler: () => {
      onSuccess(
        "Payment submitted. Subscription will activate after secure webhook confirmation.",
      );
    },
    modal: {
      ondismiss: () => {
        onFailure("Razorpay test checkout was closed before completion.");
      },
    },
  });
  checkout.open();
}
