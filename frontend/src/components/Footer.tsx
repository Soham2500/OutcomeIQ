import { Link } from "react-router-dom";

const footerLinks = [
  { label: "Privacy", path: "/privacy" },
  { label: "Terms", path: "/terms" },
  { label: "Refund Policy", path: "/refund-policy" },
  { label: "Contact", path: "/contact" },
];

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white px-5 py-5 text-sm text-slate-500 md:px-8">
      <div className="mx-auto flex max-w-[1500px] flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <p>© {new Date().getFullYear()} OutcomeIQ. Test-mode MVP for launch validation.</p>
        <nav className="flex flex-wrap gap-4">
          {footerLinks.map((link) => (
            <Link className="hover:text-brand-700" key={link.path} to={link.path}>
              {link.label}
            </Link>
          ))}
        </nav>
      </div>
    </footer>
  );
}
