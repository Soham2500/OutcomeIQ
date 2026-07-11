import { Outlet } from "react-router-dom";
import { Footer } from "./Footer";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Sidebar />
      <div className="md:pl-72">
        <Topbar />
        <main className="p-5 md:p-8">
          <div className="mx-auto max-w-[1500px]">
            <Outlet />
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
