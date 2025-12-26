import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import DotGrid from "../components/reactbits/DotGrid/DotGrid";
import RotatingText from "../components/reactbits/RotatingText/RotatingText";
import ScrollVelocity from "../components/reactbits/ScrollVelocity/ScrollVelocity";
import Carousel from "../components/reactbits/Carousel/Carousel";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import logo from "../assets/loogoo.png";

export default function Home() {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

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

  const stats = [
    { value: "10K+", label: "Drugs Analyzed", icon: "💊" },
    { value: "98%", label: "Accuracy Rate", icon: "🎯" },
    { value: "500+", label: "Research Papers", icon: "📄" },
    { value: "24/7", label: "AI Processing", icon: "🤖" }
  ];

  const features = [
    {
      icon: "🧬",
      title: "RAG-Powered Intelligence",
      description: "Retrieval-Augmented Generation combines vast biomedical knowledge with AI reasoning for precise drug insights.",
      gradient: "from-cyan-500 to-blue-600"
    },
    {
      icon: "⚡",
      title: "Accelerated Discovery",
      description: "Reduce drug repurposing timelines from years to weeks with intelligent data-driven analysis.",
      gradient: "from-purple-500 to-pink-600"
    },
    {
      icon: "🔬",
      title: "Explainable AI",
      description: "Transparent reasoning and citations ensure every recommendation is backed by verifiable research.",
      gradient: "from-emerald-500 to-teal-600"
    }
  ];

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#050816] text-white">

      {/* ================= DOT GRID BACKGROUND ================= */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <DotGrid
          dotSize={5}
          gap={15}
          baseColor="#3B3B3B"
          activeColor="#2EF8FF"
          proximity={120}
          shockRadius={250}
          shockStrength={5}
          resistance={750}
          returnDuration={1.5}
          style={{ width: "100%", height: "100%" }}
        />
      </div>

      {/* ================= GRADIENT OVERLAYS ================= */}
      <div className="fixed inset-0 z-10 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-[#050816]/80 via-[#050816]/40 to-[#050816]/90" />
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl" />
      </div>

      {/* ================= NAVBAR ================= */}
      <Navbar items={navItems} />

      {/* ================= HERO SECTION ================= */}
      <section className={`relative z-20 flex flex-col items-center px-6 pt-32 pb-20 text-center transition-all duration-1000 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>


        {/* Logo */}
        <div className="mb-6 flex items-center justify-center">
          <img
            src={logo}
            alt="Sanjeevani Logo"
            className="h-24 w-auto drop-shadow-[0_0_35px_rgba(46,248,255,0.3)] transition-transform duration-500 hover:scale-105"
          />
        </div>

        {/* Main Heading */}
        <h1 className="mb-6 text-xl font-bold leading-tight md:text-2xl lg:text-5xl">
          <span className="bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">
            Revolutionizing
          </span>
          <br />
          <span className="mt-2 inline-block">
            <RotatingText
              texts={['Drug Repurposing', 'Healthcare AI', 'Medical Discovery', 'Biomedical Research']}
              mainClassName="px-3 sm:px-4 md:px-5 bg-gradient-to-r from-cyan-400 to-blue-500 text-white overflow-hidden py-1 sm:py-2 md:py-3 justify-center rounded-xl shadow-[0_0_30px_rgba(34,211,238,0.4)]"
              staggerFrom={"last"}
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              exit={{ y: "-120%" }}
              staggerDuration={0.025}
              splitLevelClassName="overflow-hidden pb-0.5 sm:pb-1 md:pb-1"
              transition={{ type: "spring", damping: 30, stiffness: 400 }}
              rotationInterval={2500}
            />
          </span>
        </h1>

        {/* Subtitle */}
        <p className="max-w-3xl mb-10 text-lg text-gray-400 md:text-xl leading-relaxed">
          Sanjeevani leverages <span className="text-cyan-400 font-medium">Retrieval-Augmented Generation</span> and cutting-edge AI to identify new therapeutic uses for existing drugs,
          accelerating research, reducing costs, and enabling responsible healthcare innovation.
        </p> 

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            to="/login"
            className="group relative inline-flex items-center justify-center gap-2 rounded-full bg-gradient-to-r from-cyan-500 to-blue-600 px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:shadow-[0_0_40px_rgba(34,211,238,0.5)] hover:scale-105"
          >
            <span>Get Started</span>
            <svg className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
            <div className="absolute inset-0 rounded-full bg-white/20 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
          </Link>

          <Link
            to="/about1"
            className="inline-flex items-center justify-center gap-2 rounded-full border border-gray-600 bg-white/5 px-8 py-4 text-lg font-semibold text-gray-300 backdrop-blur-sm transition-all duration-300 hover:border-cyan-500/50 hover:text-white hover:bg-white/10"
          >
            <span>Learn More</span>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </section>

      {/* ================= STATS SECTION ================= */}
      <section className={`relative z-20 px-6 py-16 transition-all duration-1000 delay-300 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
        <div className="mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm transition-all duration-300 hover:border-cyan-500/30 hover:bg-white/10"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
                <div className="relative flex items-center justify-center">
                  <h3 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent mb-1">
                    {stat.value}
                  </h3>
                  <p className="text-sm text-gray-400 ml-4 text-l">{stat.label}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ================= SCROLL VELOCITY ================= */}
      <section className="relative z-30 py-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-[#050816] via-transparent to-[#050816] z-10 pointer-events-none" />
        <ScrollVelocity
          texts={[
            "AI-Powered Drug Discovery • Biomedical Intelligence • RAG Technology •",
            "Machine Learning • Research Acceleration • Healthcare Innovation •"
          ]}
          velocity={80}
          className="text-white/80"
        />
      </section>

      {/* ================= FEATURES SECTION ================= */}
      <section className={`relative z-20 px-6 py-20 transition-all duration-1000 delay-500 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
        <div className="mx-auto max-w-6xl">
          {/* Section Header */}
          <div className="text-center mb-16">
            <span className="text-cyan-400 text-sm font-semibold tracking-wider uppercase mb-4 block">Core Capabilities</span>
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                Why Choose Sanjeevani?
              </span>
            </h2>
            <p className="max-w-2xl mx-auto text-gray-400">
              Built with cutting-edge technology to transform how researchers discover new therapeutic applications for existing drugs.
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent p-8 transition-all duration-500 hover:border-white/20 hover:transform hover:-translate-y-2"
              >
                {/* Glow Effect */}
                <div className={`absolute -inset-px rounded-3xl bg-gradient-to-r ${feature.gradient} opacity-0 blur-xl transition-opacity duration-500 group-hover:opacity-20`} />

                <div className="relative">
                  {/* Icon
                  <div className={`inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-r ${feature.gradient} mb-6 text-2xl shadow-lg`}>
                    {feature.icon}
                  </div> */}

                  {/* Title */}
                  <h3 className="text-xl font-bold text-white mb-3 group-hover:text-cyan-300 transition-colors duration-300">
                    {feature.title}
                  </h3>

                  {/* Description */}
                  <p className="text-gray-400 leading-relaxed">
                    {feature.description}
                  </p>

                  {/* Learn More Link */}
                  <div className="mt-6 flex items-center text-cyan-400 text-sm font-medium opacity-0 translate-y-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-y-0">
                    <span>Explore</span>
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ================= CAROUSEL SECTION ================= */}
      <section className="relative z-30 px-6 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <span className="text-purple-400 text-sm font-semibold tracking-wider uppercase mb-4 block">How It Works</span>
            <h2 className="text-3xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
                The Sanjeevani Pipeline
              </span>
            </h2>
          </div>

          <div className="relative flex justify-center" style={{ height: "280px" }}>
            <Carousel
              baseWidth={620}
              autoplay={true}
              autoplayDelay={2500}
              pauseOnHover={true}
              loop={true}
              round={false}
            />
          </div>
        </div>
      </section>

      {/* ================= CTA SECTION ================= */}
      <section className="relative z-20 px-6 py-24">
        <div className="mx-auto max-w-4xl">
          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-cyan-500/10 via-purple-500/5 to-blue-500/10 p-12 md:p-16 text-center backdrop-blur-sm">
            {/* Decorative Elements */}
            <div className="absolute top-0 left-0 w-40 h-40 bg-cyan-500/20 rounded-full blur-3xl" />
            <div className="absolute bottom-0 right-0 w-40 h-40 bg-purple-500/20 rounded-full blur-3xl" />

            <div className="relative">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                <span className="bg-gradient-to-r from-cyan-400 via-white to-purple-400 bg-clip-text text-transparent">
                  Ready to Transform Drug Discovery?
                </span>
              </h2>
              <p className="text-gray-400 text-lg mb-8 max-w-2xl mx-auto">
                Join researchers worldwide using Sanjeevani to accelerate their biomedical research and discover new therapeutic applications.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/Login"
                  className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-8 py-4 text-lg font-semibold text-gray-900 transition-all duration-300 hover:shadow-[0_0_40px_rgba(255,255,255,0.3)] hover:scale-105"
                >
                  <span>Start Free Trial</span>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </Link>

                <Link
                  to="/about"
                  className="inline-flex items-center justify-center gap-2 rounded-full border border-white/30 px-8 py-4 text-lg font-semibold text-white transition-all duration-300 hover:border-white hover:bg-white/10"
                >
                  <span>Meet the Team</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <Footer />
    </div>
  );
}
