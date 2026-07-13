import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Footer } from "./Footer";
import { GradientBackground } from "./GradientBackground";
import { PremiumMouseGlow } from "./PremiumMouseGlow";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";

export function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <GradientBackground />
      <PremiumMouseGlow />
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="md:pl-80">
        <Topbar onMenuClick={() => setSidebarOpen(true)} />
        <main className="p-4 md:p-8">
          <div className="mx-auto max-w-[1500px]">
            <AnimatePresence mode="wait">
              <motion.div
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                initial={{ opacity: 0, y: 12 }}
                key={location.pathname}
                transition={{ duration: 0.22, ease: "easeOut" }}
              >
                <Outlet />
              </motion.div>
            </AnimatePresence>
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
