interface LoadingStateProps {
  message?: string;
}

export function LoadingState({
  message = "Loading OutcomeIQ data…",
}: LoadingStateProps) {
  return (
    <div className="flex min-h-48 items-center justify-center rounded-3xl border border-white/70 bg-white/80 p-8 text-sm text-slate-500 shadow-card backdrop-blur">
      <span className="mr-3 h-5 w-5 animate-spin rounded-full border-2 border-brand-100 border-t-brand-600" />
      {message}
    </div>
  );
}
