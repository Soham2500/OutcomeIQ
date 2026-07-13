import { type ReactNode, useEffect } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";

interface ModalProps {
  title: string;
  description?: string;
  open: boolean;
  onClose: () => void;
  children: ReactNode;
  footer?: ReactNode;
}

export function Modal({ title, description, open, onClose, children, footer }: ModalProps) {
  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        onClose();
      }
    }
    if (open) {
      document.addEventListener("keydown", handleKeyDown);
    }
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [onClose, open]);

  return (
    <AnimatePresence>
      {open ? (
        <div className="fixed inset-0 z-[70] flex items-center justify-center p-4">
          <motion.button
            aria-label="Close dialog"
            animate={{ opacity: 1 }}
            className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm"
            exit={{ opacity: 0 }}
            initial={{ opacity: 0 }}
            onClick={onClose}
            type="button"
          />
          <motion.section
            animate={{ opacity: 1, scale: 1, y: 0 }}
            aria-modal="true"
            className="relative w-full max-w-xl rounded-3xl border border-white/70 bg-white p-6 shadow-2xl"
            exit={{ opacity: 0, scale: 0.98, y: 16 }}
            initial={{ opacity: 0, scale: 0.98, y: 16 }}
            role="dialog"
            transition={{ duration: 0.22, ease: "easeOut" }}
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold text-slate-950">{title}</h2>
                {description ? (
                  <p className="mt-1 text-sm leading-6 text-slate-500">{description}</p>
                ) : null}
              </div>
              <button
                aria-label="Close dialog"
                className="flex h-10 w-10 items-center justify-center rounded-2xl border border-slate-200 text-slate-500 transition hover:bg-slate-50 hover:text-slate-900"
                onClick={onClose}
                type="button"
              >
                <X aria-hidden="true" className="h-5 w-5" />
              </button>
            </div>
            <div className="mt-5">{children}</div>
            {footer ? <div className="mt-6 flex justify-end gap-3">{footer}</div> : null}
          </motion.section>
        </div>
      ) : null}
    </AnimatePresence>
  );
}
