import Navbar from "../components/Navbar";
import SplitText from "../components/reactbits/SplitText/SplitText";
import Orb from "../components/reactbits/Orb/Orb";
import Footer from "../components/Footer";

export default function Dashboard() {
  const name = localStorage.getItem("name");

  const logout = () => {
    localStorage.clear();
    window.location.href = "/login";
  };
  const navItems = [
    {
      label: "About",
      bgColor: "#0D0716",
      textColor: "#ffffff",
      links: [
        { label: "What we do", ariaLabel: "About project", to: "/about1" },
        { label: "Problem we solve", ariaLabel: "About project", to: "/about1" },
        { label: "Why Drug Repurposing", ariaLabel: "About project", to: "/about1" }
      ]
    },
    {
      label: "Technology",
      bgColor: "#170D27",
      textColor: "#ffffff",
      links: [
        { label: "AI Models", ariaLabel: "AI Models", to: "/technology" },
        { label: "Tech Stack", ariaLabel: "Tech Stack", to: "/technology" }
      ]
    },
    {
      label: "Contact",
      bgColor: "#0f0029ff",
      textColor: "#ffffff",
      links: [
        { label: "Email", ariaLabel: "Email", to: "/about" },
        { label: "LinkedIn", ariaLabel: "LinkedIn", to: "/about" },
        { label: "Github", ariaLabel: "Github", to: "/about" }
      ]
    }
  ];

  return (
    <div className="relative min-h-screen bg-[#050816] overflow-hidden text-white">

      {/* ========== NAVBAR ========== */}
      <div className="relative z-50">
        <Navbar items={navItems} isLoggedIn={true} />
      </div>

      {/* ========== CONTENT BELOW NAVBAR ========== */}
      <section className="relative z-10 px-8 pt-32">

        {/* SPLIT TEXT */}
        <SplitText
          text={`Welcome ${name || "User"}!`}
          className="pl-83 text-3xl md:text-4xl font-semibold text-left"
          delay={70}
          duration={2}
          ease="elastic.out(1, 0.3)"
          splitType="chars"
          from={{ opacity: 0, y: 30 }}
          to={{ opacity: 1, y: 0 }}
          threshold={0.1}
          rootMargin="-100px"
          textAlign="left"
        />

        {/* ========== ORB SECTION ========== */}
        <div className="relative h-[600px] w-full flex items-center justify-center">

          {/* ORB */}
          <div className="absolute inset-0 z-0">
            <Orb
              hoverIntensity={1}
              rotateOnHover={true}
              hue={0}
              forceHoverState={false}
            />
          </div>

          {/* SEARCH BOX (CENTER OF ORB) */}
          <div className="relative z-10 w-full max-w-xl px-6">

            {/* Heading with gradient */}
            <h2 className="text-xl md:text-2xl font-bold text-center mb-8">
              <span className="bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent">
                Ask Drug Repurposing AI
              </span>
            </h2>

            {/* Search Container with animated border */}
            <div className="relative group">
              {/* Animated gradient border */}
              <div className="absolute -inset-[2px] bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500 rounded-2xl opacity-60 blur-sm group-hover:opacity-100 group-hover:blur-md transition-all duration-500 animate-[spin_4s_linear_infinite]"
                style={{ backgroundSize: '200% 200%', animation: 'gradient-shift 3s ease infinite' }} />

              {/* Glass container */}
              <div className="relative bg-white/10 backdrop-blur-xl rounded-xl p-1.5 border border-white/20 shadow-[0_8px_32px_rgba(139,92,246,0.3)]">
                <div className="flex items-center gap-3">
                  {/* Search icon */}
                  <div className="pl-3 text-purple-400">
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>

                  {/* Input field */}
                  <input
                    type="text"
                    placeholder="Search for drug repurposing insights..."
                    className="
                      flex-1
                      py-2.5 pr-3
                      bg-transparent
                      text-white
                      placeholder-white/50
                      outline-none
                      text-base
                      font-light
                    "
                  />

                  {/* Search button */}
                  <button
                    className="
                      group/btn
                      relative
                      px-5 py-2
                      rounded-lg
                      bg-gradient-to-r from-purple-600 via-pink-500 to-purple-600
                      text-white text-sm font-semibold
                      overflow-hidden
                      transition-all duration-300
                      hover:shadow-[0_0_30px_rgba(168,85,247,0.6)]
                      hover:scale-105
                      active:scale-95
                    "
                    style={{ backgroundSize: '200% 100%' }}
                  >
                    {/* Shine effect */}
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover/btn:translate-x-full transition-transform duration-700" />

                    <span className="relative flex items-center gap-2">
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Search
                    </span>
                  </button>
                </div>
              </div>
            </div>

            {/* Example text with better styling */}
            <div className="mt-6 text-center">
              <p className="text-sm text-gray-400">
                <span className="text-purple-400/80">Try: </span>{" "}
                <span className="italic text-white/60 hover:text-white/90 cursor-pointer transition-colors duration-300">
                   "Existing drugs for Alzheimer's disease"
                </span>
              </p>

              {/* Quick suggestion chips */}
              <div className="flex flex-wrap justify-center gap-2 mt-4">
                {['Cancer treatments', 'Rare diseases', 'COVID-19'].map((chip) => (
                  <button
                    key={chip}
                    className="px-3 py-1.5 text-xs rounded-full bg-white/5 border border-white/10 text-gray-400 hover:bg-white/10 hover:text-white hover:border-purple-500/50 transition-all duration-300"
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>

          </div>
        </div>
        <Footer />
      </section>
    </div>
  );
}
