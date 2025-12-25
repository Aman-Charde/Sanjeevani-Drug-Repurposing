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
              <h4 className="mb-3 font-semibold text-white">Product</h4>
              <ul className="space-y-2">
                <li className="hover:text-cyan-400 cursor-pointer">Features</li>
                <li className="hover:text-cyan-400 cursor-pointer">Technology</li>
                <li className="hover:text-cyan-400 cursor-pointer">Use Cases</li>
              </ul>
            </div>

            <div>
              <h4 className="mb-3 font-semibold text-white">Company</h4>
              <ul className="space-y-2">
                <li className="hover:text-cyan-400 cursor-pointer">About</li>
                <li className="hover:text-cyan-400 cursor-pointer">Research</li>
                <li className="hover:text-cyan-400 cursor-pointer">Contact</li>
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
            Built with <span className="text-red-400">♥</span> using AI & Research
          </p>
        </div>

      </div>
    </footer>
  );
}
