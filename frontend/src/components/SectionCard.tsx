import type { ReactNode } from "react";

interface SectionCardProps {
  title?: string;
  description?: string;
  children: ReactNode;
  actions?: ReactNode;
  tone?: "default" | "brand" | "dark";
}

const toneClasses = {
  default: "glass-panel text-slate-900",
  brand: "border-brand-200 bg-gradient-to-br from-brand-50/95 to-cyan-50/90 text-slate-950 shadow-glow",
  dark: "border-white/10 bg-slate-950/95 text-white shadow-2xl shadow-slate-950/20",
};

export function SectionCard({
  title,
  description,
  children,
  actions,
  tone = "default",
}: SectionCardProps) {
  return (
    <section className={`rounded-3xl border p-5 md:p-6 ${toneClasses[tone]}`}>
      {(title || description || actions) ? (
        <div className="mb-5 flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
          <div>
            {title ? <h2 className="text-lg font-semibold tracking-tight">{title}</h2> : null}
            {description ? (
              <p
                className={`mt-1 text-sm leading-6 ${
                  tone === "dark" ? "text-slate-300" : "text-slate-500"
                }`}
              >
                {description}
              </p>
            ) : null}
          </div>
          {actions ? <div className="shrink-0">{actions}</div> : null}
        </div>
      ) : null}
      {children}
    </section>
  );
}
