import { NavLink } from "react-router-dom";
import { AppLogo } from "./AppLogo";

const navigation = [
  { label: "Dashboard", path: "/dashboard", icon: "◫" },
  { label: "Projects", path: "/projects", icon: "▣" },
  { label: "Workflows", path: "/workflows", icon: "↻" },
  { label: "Recommendations", path: "/recommendations", icon: "◇" },
  { label: "Demo Guide", path: "/demo-guide", icon: "▷" },
];

export function Sidebar() {
  return (
    <aside className="border-b border-slate-800 bg-slate-950 px-4 py-4 text-white md:fixed md:inset-y-0 md:z-30 md:w-72 md:border-b-0 md:border-r md:px-5 md:py-6">
      <div className="mb-4 px-2 md:mb-8">
        <AppLogo inverse />
      </div>
      <nav className="flex gap-2 overflow-x-auto md:flex-col md:overflow-visible">
        {navigation.map((item) => (
          <NavLink
            className={({ isActive }) =>
              `flex shrink-0 items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                isActive
                  ? "bg-brand-600 text-white"
                  : "text-slate-300 hover:bg-slate-900 hover:text-white"
              }`
            }
            key={item.path}
            to={item.path}
          >
            <span aria-hidden="true">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div className="mt-8 hidden rounded-xl border border-slate-800 bg-slate-900/70 p-4 md:block">
        <p className="text-xs font-semibold uppercase tracking-wider text-brand-100">
          Core proof
        </p>
        <p className="mt-2 text-xs leading-5 text-slate-400">
          Compare AI spend with verified business success—not requests alone.
        </p>
      </div>
    </aside>
  );
}
