import { createContext, type ReactNode, useContext, useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { CheckCircle2, Info, TriangleAlert, X, XCircle } from "lucide-react";

type ToastTone = "success" | "error" | "info" | "warning";

interface ToastMessage {
  id: number;
  tone: ToastTone;
  title: string;
  description?: string;
}

interface ToastContextValue {
  notify: (message: Omit<ToastMessage, "id">) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

const toneClasses: Record<ToastTone, string> = {
  success: "border-emerald-200 bg-emerald-50 text-emerald-900",
  error: "border-rose-200 bg-rose-50 text-rose-900",
  info: "border-brand-200 bg-brand-50 text-brand-900",
  warning: "border-amber-200 bg-amber-50 text-amber-900",
};

const icons: Record<ToastTone, typeof CheckCircle2> = {
  success: CheckCircle2,
  error: XCircle,
  info: Info,
  warning: TriangleAlert,
};

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const value = useMemo<ToastContextValue>(
    () => ({
      notify(message) {
        const id = Date.now() + Math.random();
        setToasts((current) => [...current, { ...message, id }]);
        window.setTimeout(() => {
          setToasts((current) => current.filter((toast) => toast.id !== id));
        }, 4200);
      },
    }),
    [],
  );

  function dismiss(id: number) {
    setToasts((current) => current.filter((toast) => toast.id !== id));
  }

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div
        aria-live="polite"
        className="fixed right-4 top-4 z-[80] flex w-[calc(100%-2rem)] max-w-sm flex-col gap-3"
      >
        <AnimatePresence>
          {toasts.map((toast) => {
            const Icon = icons[toast.tone];
            return (
              <motion.div
                animate={{ opacity: 1, x: 0, scale: 1 }}
                className={`rounded-2xl border p-4 shadow-soft backdrop-blur ${toneClasses[toast.tone]}`}
                exit={{ opacity: 0, x: 24, scale: 0.98 }}
                initial={{ opacity: 0, x: 24, scale: 0.98 }}
                key={toast.id}
                transition={{ duration: 0.22, ease: "easeOut" }}
              >
                <div className="flex gap-3">
                  <Icon aria-hidden="true" className="mt-0.5 h-5 w-5 shrink-0" />
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold">{toast.title}</p>
                    {toast.description ? (
                      <p className="mt-1 text-sm opacity-80">{toast.description}</p>
                    ) : null}
                  </div>
                  <button
                    aria-label="Dismiss notification"
                    className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full opacity-70 transition hover:bg-white/60 hover:opacity-100"
                    onClick={() => dismiss(toast.id)}
                    type="button"
                  >
                    <X aria-hidden="true" className="h-4 w-4" />
                  </button>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used inside ToastProvider.");
  }
  return context;
}
