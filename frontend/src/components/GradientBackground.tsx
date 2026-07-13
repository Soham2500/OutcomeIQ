export function GradientBackground() {
  return (
    <div aria-hidden="true" className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div className="animate-ambient absolute -left-32 top-[-12rem] h-96 w-96 rounded-full bg-brand-500/16 blur-3xl" />
      <div className="animate-ambient absolute right-[-10rem] top-20 h-[28rem] w-[28rem] rounded-full bg-cyan-400/12 blur-3xl [animation-delay:1.2s]" />
      <div className="absolute bottom-[-14rem] left-1/2 h-[30rem] w-[30rem] -translate-x-1/2 rounded-full bg-violet-500/10 blur-3xl" />
      <div className="absolute inset-0 bg-[linear-gradient(rgba(15,23,42,0.025)_1px,transparent_1px),linear-gradient(90deg,rgba(15,23,42,0.025)_1px,transparent_1px)] bg-[size:42px_42px]" />
    </div>
  );
}
