interface SkeletonCardProps {
  lines?: number;
}

export function SkeletonCard({ lines = 3 }: SkeletonCardProps) {
  return (
    <div className="premium-card p-5">
      <div className="skeleton-shimmer h-4 w-28 rounded-full" />
      <div className="skeleton-shimmer mt-4 h-8 w-40 rounded-xl" />
      <div className="mt-5 space-y-3">
        {Array.from({ length: lines }).map((_, index) => (
          <div
            className="skeleton-shimmer h-3 rounded-full"
            key={index}
            style={{ width: `${92 - index * 12}%` }}
          />
        ))}
      </div>
    </div>
  );
}
