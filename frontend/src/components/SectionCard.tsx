import type { ReactNode } from "react";

interface SectionCardProps {
  title?: string;
  description?: string;
  children: ReactNode;
  actions?: ReactNode;
  tone?: "default" | "brand" | "dark";
}

const toneClasses = {
  default: "border-slate-200 bg-white text-slate-900",
  brand: "border-brand-100 bg-brand-50 text-slate-950",
  dark: "border-slate-800 bg-slate-950 text-white",
};

export function SectionCard({
  title,
  description,
  children,
  actions,
  tone = "default",
}: SectionCardProps) {
  return (
    <section className={`rounded-xl border p-5 shadow-card md:p-6 ${toneClasses[tone]}`}>
      {(title || description || actions) ? (
        <div className="mb-5 flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
          <div>
            {title ? <h2 className="font-semibold">{title}</h2> : null}
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
