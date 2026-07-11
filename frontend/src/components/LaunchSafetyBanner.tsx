interface LaunchSafetyBannerProps {
  message: string;
}

export function LaunchSafetyBanner({ message }: LaunchSafetyBannerProps) {
  return (
    <section className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900 shadow-sm">
      <p className="font-semibold">Launch safety notice</p>
      <p className="mt-1 leading-6">{message}</p>
    </section>
  );
}
