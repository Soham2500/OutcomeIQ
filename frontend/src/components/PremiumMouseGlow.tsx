import { useEffect, useRef } from "react";

export function PremiumMouseGlow() {
  const glowRef = useRef<HTMLDivElement | null>(null);
  const frameRef = useRef<number | null>(null);
  const positionRef = useRef({ x: -9999, y: -9999 });

  useEffect(() => {
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const pointerFine = window.matchMedia("(pointer: fine)");
    if (reduceMotion.matches || !pointerFine.matches) {
      return;
    }

    function render() {
      frameRef.current = null;
      const element = glowRef.current;
      if (!element) {
        return;
      }
      element.style.setProperty("--mouse-x", `${positionRef.current.x}px`);
      element.style.setProperty("--mouse-y", `${positionRef.current.y}px`);
    }

    function handlePointerMove(event: PointerEvent) {
      positionRef.current = { x: event.clientX, y: event.clientY };
      if (frameRef.current === null) {
        frameRef.current = window.requestAnimationFrame(render);
      }
    }

    window.addEventListener("pointermove", handlePointerMove, { passive: true });
    return () => {
      window.removeEventListener("pointermove", handlePointerMove);
      if (frameRef.current !== null) {
        window.cancelAnimationFrame(frameRef.current);
      }
    };
  }, []);

  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 z-0 hidden opacity-70 mix-blend-screen md:block"
      ref={glowRef}
      style={{
        background:
          "radial-gradient(520px circle at var(--mouse-x, -9999px) var(--mouse-y, -9999px), rgba(99, 102, 241, 0.14), rgba(14, 165, 233, 0.08) 36%, transparent 68%)",
      }}
    />
  );
}
