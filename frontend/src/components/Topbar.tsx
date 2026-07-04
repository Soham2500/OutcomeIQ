import { useNavigate } from "react-router-dom";
import { TOKEN_KEY } from "../api/client";

export function Topbar() {
  const navigate = useNavigate();

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    navigate("/login", { replace: true });
  }

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-5 md:px-8">
      <div>
        <p className="text-xs font-medium uppercase tracking-wider text-brand-600">
          Outcome-aware decisions
        </p>
        <p className="font-semibold text-slate-900">OutcomeIQ</p>
      </div>
      <button className="secondary-button" onClick={logout} type="button">
        Log out
      </button>
    </header>
  );
}
