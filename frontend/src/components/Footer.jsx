import { Link } from "react-router-dom";
import logo from "../assets/loogoo.png";

export default function Footer() {
  return (
    <footer className="relative z-30 border-t border-white/10 bg-[#050816] px-6 pt-16 pb-10 text-gray-300">
      <div className="mx-auto max-w-6xl">

        {/* ================= TOP SECTION ================= */}
        <div className="flex flex-col items-center justify-between gap-10 md:flex-row">

          {/* LOGO + DESCRIPTION */}
          <div className="max-w-md text-center md:text-left">
            <div className="mb-4 flex items-center justify-center gap-3 md:justify-start">
              <img
                src={logo}
                alt="Sanjeevani Logo"
                className="h-20 w-auto"
              />
            </div>

            <p className="text-sm leading-relaxed text-gray-400">
              Sanjeevani is an AI-powered drug repurposing platform designed to
              accelerate biomedical research and enable faster, cost-effective
              drug discovery.
            </p>
          </div>

          {/* LINKS */}
          <div className="flex gap-16 text-sm">

            <div>
              <h4 className="mb-3 font-semibold text-white">Company</h4>
              <ul className="space-y-2">
                <li><Link to="/about1" className="hover:text-cyan-400 cursor-pointer transition-colors">About</Link></li>
                <li><Link to="/technology" className="hover:text-cyan-400 cursor-pointer transition-colors">Research</Link></li>
                <li><Link to="/about" className="hover:text-cyan-400 cursor-pointer transition-colors">Contact</Link></li>
              </ul>
            </div>

          </div>
        </div>

        {/* ================= DIVIDER ================= */}
        <div className="my-10 h-px w-full bg-white/10" />

        {/* ================= BOTTOM ================= */}
        <div className="flex flex-col items-center justify-between gap-4 text-xs md:flex-row">
          <p>
            © {new Date().getFullYear()}{" "}
            <span className="text-white font-medium">Sanjeevani</span>.
            All rights reserved.
          </p>

          <p className="text-gray-400">
            Built with <span className="text-red-500">♥</span>
          </p>
        </div>

      </div>
    </footer>
  );
}
