import { NavLink } from "react-router-dom";

const navigation = [
  { label: "Dashboard", path: "/dashboard", icon: "◫" },
  { label: "Projects", path: "/projects", icon: "▣" },
  { label: "Recommendations", path: "/recommendations", icon: "◇" },
];

export function Sidebar() {
  return (
    <aside className="border-b border-slate-800 bg-slate-950 px-4 py-4 text-white md:fixed md:inset-y-0 md:w-64 md:border-b-0 md:border-r md:px-5 md:py-6">
      <div className="mb-4 flex items-center gap-3 px-2 md:mb-8">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-500 font-bold">
          O
        </div>
        <div>
          <p className="font-semibold">OutcomeIQ</p>
          <p className="text-xs text-slate-400">Outcome-aware FinOps</p>
        </div>
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
    </aside>
  );
}
