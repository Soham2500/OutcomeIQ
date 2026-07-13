interface AppLogoProps {
  inverse?: boolean;
  compact?: boolean;
}

export function AppLogo({ inverse = false, compact = false }: AppLogoProps) {
  return (
    <div className="flex items-center gap-3">
      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-brand-500 via-violet-600 to-cyan-400 font-bold text-white shadow-glow">
        OQ
      </div>
      <div className={compact ? "hidden lg:block" : "block"}>
        <p
          className={`font-semibold tracking-tight ${inverse ? "text-white" : "text-slate-950"}`}
        >
          OutcomeIQ
        </p>
        <p
          className={`text-[11px] ${inverse ? "text-slate-400" : "text-slate-500"}`}
        >
          Outcome-aware AI FinOps Platform
        </p>
      </div>
    </div>
  );
}
