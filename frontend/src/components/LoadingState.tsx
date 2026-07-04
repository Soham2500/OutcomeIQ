interface LoadingStateProps {
  message?: string;
}

export function LoadingState({
  message = "Loading OutcomeIQ data…",
}: LoadingStateProps) {
  return (
    <div className="flex min-h-48 items-center justify-center rounded-xl border border-slate-200 bg-white p-8 text-sm text-slate-500 shadow-card">
      <span className="mr-3 h-5 w-5 animate-spin rounded-full border-2 border-brand-100 border-t-brand-600" />
      {message}
    </div>
  );
}
