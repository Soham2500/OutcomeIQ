import { NavLink } from "react-router-dom";
import {
  BarChart3,
  Bot,
  CreditCard,
  Gauge,
  LayoutDashboard,
  Lightbulb,
  Rocket,
  Settings,
  Workflow,
  X,
} from "lucide-react";
import { AppLogo } from "./AppLogo";

const navigation = [
  { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { label: "Projects", path: "/projects", icon: Gauge },
  { label: "Workflows", path: "/workflows", icon: Workflow },
  { label: "Run AI Test", path: "/ai-runs", icon: Bot },
  { label: "Analytics", path: "/analytics", icon: BarChart3 },
  { label: "Recommendations", path: "/recommendations", icon: Lightbulb },
  { label: "Pricing", path: "/pricing", icon: Rocket },
  { label: "Billing", path: "/billing", icon: CreditCard },
  { label: "Demo Guide", path: "/demo-guide", icon: Settings },
  { label: "Launch Readiness", path: "/launch-readiness", icon: Rocket },
];

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

export function Sidebar({ open, onClose }: SidebarProps) {
  return (
    <>
      <button
        aria-label="Close navigation overlay"
        className={`fixed inset-0 z-40 bg-slate-950/60 backdrop-blur-sm transition md:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
        onClick={onClose}
        type="button"
      />
      <aside
        className={`fixed inset-y-0 left-0 z-50 flex w-80 max-w-[86vw] flex-col border-r border-white/10 bg-slate-950/95 px-4 py-5 text-white shadow-2xl shadow-slate-950/40 backdrop-blur-xl transition-transform duration-300 md:translate-x-0 ${
          open ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="flex items-center justify-between gap-3 px-2">
          <AppLogo inverse />
          <button
            aria-label="Close navigation"
            className="flex h-10 w-10 items-center justify-center rounded-2xl border border-white/10 text-slate-300 transition hover:bg-white/10 hover:text-white md:hidden"
            onClick={onClose}
            type="button"
          >
            <X aria-hidden="true" className="h-5 w-5" />
          </button>
        </div>

        <div className="mt-6 rounded-3xl border border-white/10 bg-white/[0.06] p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200">
            AI FinOps Control
          </p>
          <p className="mt-2 text-sm leading-6 text-slate-300">
            Tie every token, retry and model call to verified business outcomes.
          </p>
        </div>

        <nav className="mt-6 flex-1 space-y-1 overflow-y-auto pr-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                className={({ isActive }) =>
                  `group flex min-h-11 items-center gap-3 rounded-2xl px-3 py-2.5 text-sm font-semibold transition duration-200 ${
                    isActive
                      ? "bg-white text-slate-950 shadow-glow"
                      : "text-slate-300 hover:bg-white/10 hover:text-white"
                  }`
                }
                key={item.path}
                onClick={onClose}
                to={item.path}
              >
                <Icon aria-hidden="true" className="h-5 w-5 shrink-0" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="mt-5 rounded-3xl border border-cyan-300/20 bg-gradient-to-br from-brand-600/35 to-cyan-500/20 p-4">
          <p className="text-sm font-semibold text-white">Portfolio-ready proof</p>
          <p className="mt-2 text-xs leading-5 text-slate-300">
            Show why cost per request and cost per successful outcome lead to different decisions.
          </p>
        </div>
      </aside>
    </>
  );
}
