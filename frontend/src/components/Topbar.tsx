import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getCurrentUser } from "../api/authApi";
import { TOKEN_KEY } from "../api/client";

const pageTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/projects": "Projects",
  "/workflows": "Workflows",
  "/recommendations": "Recommendations",
  "/demo-guide": "Demo Guide",
};

export function Topbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [userEmail, setUserEmail] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    getCurrentUser()
      .then((user) => {
        if (active) {
          setUserEmail(user.email);
        }
      })
      .catch(() => {
        if (active) {
          setUserEmail(null);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    navigate("/login", { replace: true });
  }

  return (
    <header className="sticky top-0 z-20 flex min-h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-5 backdrop-blur md:px-8">
      <div>
        <p className="text-xs font-medium uppercase tracking-wider text-brand-600">
          OutcomeIQ
        </p>
        <p className="font-semibold text-slate-900">
          {pageTitles[location.pathname] ?? "Outcome-aware decisions"}
        </p>
      </div>
      <div className="flex items-center gap-3">
        <div className="hidden text-right sm:block">
          <p className="text-xs text-slate-400">Signed in as</p>
          <p className="max-w-56 truncate text-sm font-medium text-slate-700">
            {userEmail ?? "Authenticated user"}
          </p>
        </div>
        <button className="secondary-button" onClick={logout} type="button">
          Log out
        </button>
      </div>
    </header>
  );
}
