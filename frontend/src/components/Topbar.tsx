import { useEffect, useState } from "react";
import { Menu, Search, ShieldCheck, UserRound } from "lucide-react";
import { useLocation, useNavigate } from "react-router-dom";
import { getCurrentUser } from "../api/authApi";
import { getMyBilling } from "../api/billingApi";
import { TOKEN_KEY } from "../api/client";
import { Badge } from "./Badge";

const pageTitles: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/projects": "Projects",
  "/workflows": "Workflows",
  "/ai-runs": "Run AI Test",
  "/analytics": "Analytics",
  "/recommendations": "Recommendations",
  "/pricing": "Pricing",
  "/billing": "Billing",
  "/demo-guide": "Demo Guide",
  "/launch-readiness": "Launch Readiness",
};

interface TopbarProps {
  onMenuClick: () => void;
}

export function Topbar({ onMenuClick }: TopbarProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [planName, setPlanName] = useState<string | null>(null);

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

  useEffect(() => {
    let active = true;
    getMyBilling()
      .then((billing) => {
        if (active) {
          setPlanName(billing.plan.name);
        }
      })
      .catch(() => {
        if (active) {
          setPlanName(null);
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
    <header className="sticky top-0 z-30 border-b border-white/60 bg-white/75 px-4 py-3 backdrop-blur-xl md:px-8">
      <div className="flex items-center justify-between gap-4">
        <div className="flex min-w-0 items-center gap-3">
          <button
            aria-label="Open navigation"
            className="flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-700 shadow-sm transition hover:bg-brand-50 hover:text-brand-700 md:hidden"
            onClick={onMenuClick}
            type="button"
          >
            <Menu aria-hidden="true" className="h-5 w-5" />
          </button>
          <div className="min-w-0">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-brand-600">
              OutcomeIQ
            </p>
            <p className="truncate text-base font-semibold text-slate-950">
              {pageTitles[location.pathname] ?? "Outcome-aware decisions"}
            </p>
          </div>
        </div>

        <div className="hidden min-w-0 flex-1 justify-center lg:flex">
          <div className="flex w-full max-w-md items-center gap-2 rounded-2xl border border-slate-200 bg-white/70 px-3 py-2 text-sm text-slate-400 shadow-sm">
            <Search aria-hidden="true" className="h-4 w-4" />
            <span>Search-ready command center</span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {planName ? <Badge tone="brand">{planName}</Badge> : null}
          <div className="hidden items-center gap-3 rounded-2xl border border-slate-200 bg-white/75 px-3 py-2 shadow-sm sm:flex">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-950 text-white">
              <UserRound aria-hidden="true" className="h-4 w-4" />
            </div>
            <div className="min-w-0">
              <p className="flex items-center gap-1 text-xs text-emerald-600">
                <ShieldCheck aria-hidden="true" className="h-3.5 w-3.5" />
                Secure session
              </p>
              <p className="max-w-44 truncate text-sm font-semibold text-slate-800">
                {userEmail ?? "Authenticated user"}
              </p>
            </div>
          </div>
          <button className="secondary-button" onClick={logout} type="button">
            Log out
          </button>
        </div>
      </div>
    </header>
  );
}
