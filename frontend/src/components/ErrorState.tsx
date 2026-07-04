interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="rounded-xl border border-rose-200 bg-rose-50 p-5">
      <p className="font-semibold text-rose-800">Something needs attention</p>
      <p className="mt-1 text-sm text-rose-700">{message}</p>
      {onRetry ? (
        <button className="secondary-button mt-4" onClick={onRetry} type="button">
          Try again
        </button>
      ) : null}
    </div>
  );
}
