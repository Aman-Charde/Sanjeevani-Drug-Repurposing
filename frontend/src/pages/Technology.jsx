import { Link } from 'react-router-dom';
import { SiReact, SiNextdotjs, SiTypescript, SiTailwindcss } from 'react-icons/si';
import LogoLoop from '../components/reactbits/LogoLoop/LogoLoop';

const techLogos = [
  { node: <SiReact />, title: "React", href: "https://react.dev" },
  { node: <SiNextdotjs />, title: "Next.js", href: "https://nextjs.org" },
  { node: <SiTypescript />, title: "TypeScript", href: "https://www.typescriptlang.org" },
  { node: <SiTailwindcss />, title: "Tailwind CSS", href: "https://tailwindcss.com" },
];

// Alternative with image sources
const imageLogos = [
  { src: "/logos/company1.png", alt: "Company 1", href: "https://company1.com" },
  { src: "/logos/company2.png", alt: "Company 2", href: "https://company2.com" },
  { src: "/logos/company3.png", alt: "Company 3", href: "https://company3.com" },
];

const Technology = () => {
  return (
    <div className="min-h-screen bg-[#050816] text-white">
      {/* Hero Section */}
      <section className="relative px-6 py-20 md:px-10 lg:px-20 overflow-hidden">
        {/* Back Button */}
        <Link
          to="/"
          className="absolute top-6 left-6 md:left-10 z-20 group flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-cyan-500/50 transition-all duration-300"
        >
          <span className="text-lg group-hover:-translate-x-1 transition-transform duration-300">←</span>
          <span className="text-sm font-medium text-gray-300 group-hover:text-white transition-colors duration-300">Back to Home</span>
        </Link>

        {/* Background decorative elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>

        <div className="relative z-10 max-w-6xl mx-auto text-center">
          <span className="text-sm font-semibold text-cyan-400 uppercase tracking-wider">Our Stack</span>
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mt-4 mb-6 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
            Technology <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Stack</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Sanjeevani is built using modern web technologies and an
            AI-powered Retrieval-Augmented Generation (RAG) approach to
            enable intelligent drug repurposing insights.
          </p>
        </div>
      </section>

      {/* AI Models Section */}
      <section className="px-6 py-16 md:px-10 lg:px-20">
        <div className="max-w-6xl mx-auto">
          <div className="group relative p-8 md:p-10 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-purple-500/50 transition-all duration-300">
            {/* Glow effect on hover */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-purple-500/0 to-pink-500/0 group-hover:from-purple-500/5 group-hover:to-pink-500/5 transition-all duration-300"></div>

            <div className="relative z-10">
              <span className="text-sm font-semibold text-purple-400 uppercase tracking-wider">AI Architecture</span>
              <h2 className="text-3xl md:text-4xl font-bold mt-2 mb-6 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                AI Models – Retrieval-Augmented Generation (RAG)
              </h2>

              <p className="text-gray-300 leading-relaxed text-lg mb-4">
                Sanjeevani uses a Retrieval-Augmented Generation (RAG) approach
                to combine information retrieval with large language models.
                Instead of relying only on a pre-trained model, the system
                retrieves relevant biomedical and drug-related information
                from a structured knowledge base before generating responses.
              </p>

              <p className="text-gray-300 leading-relaxed text-lg mb-6">
                This approach improves accuracy, reduces hallucinations, and
                ensures that the generated insights are grounded in verified
                drug and disease data.
              </p>

              <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">🔍</span>
                  <span className="text-gray-300">Retrieves relevant drug and disease information</span>
                </li>
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">📊</span>
                  <span className="text-gray-300">Augments model responses with real data</span>
                </li>
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">✅</span>
                  <span className="text-gray-300">Improves reliability and explainability</span>
                </li>
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">🎯</span>
                  <span className="text-gray-300">Supports research-oriented decision making</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Logo Loop Section */}
      <section className="px-6 py-8 md:px-10 lg:px-20">
        <div className="max-w-6xl mx-auto">
          <div style={{ height: '69px', position: 'relative', overflow: 'hidden' }}>
            <LogoLoop
              logos={techLogos}
              speed={120}
              direction="left"
              logoHeight={60}
              gap={40}
              hoverSpeed={10}
              scaleOnHover
              fadeOut
              fadeOutColor="#050816"
              ariaLabel="Technology partners"
            />
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="px-6 py-16 md:px-10 lg:px-20">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-sm font-semibold text-cyan-400 uppercase tracking-wider">Built With</span>
            <h2 className="text-4xl md:text-5xl font-bold mt-2 mb-4 bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-500 bg-clip-text text-transparent">
              Tech Stack – MERN
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              A powerful combination of modern technologies for scalable, performant applications
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Frontend */}
            <div className="group relative p-8 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-blue-500/50 transition-all duration-300 hover:transform hover:-translate-y-1">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-blue-500/0 to-cyan-500/0 group-hover:from-blue-500/5 group-hover:to-cyan-500/5 transition-all duration-300"></div>
              <div className="relative z-10">
                <div className="text-4xl mb-4">⚛️</div>
                <h3 className="text-xl font-bold mb-3 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  Frontend
                </h3>
                <ul className="text-gray-300 space-y-2">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                    React.js – Component-based UI
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                    Tailwind CSS – Utility-first styling
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
                    Responsive and research-friendly design
                  </li>
                </ul>
              </div>
            </div>

            {/* Backend */}
            <div className="group relative p-8 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-green-500/50 transition-all duration-300 hover:transform hover:-translate-y-1">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-green-500/0 to-emerald-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
              <div className="relative z-10">
                <div className="text-4xl mb-4">🖥️</div>
                <h3 className="text-xl font-bold mb-3 bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                  Backend
                </h3>
                <ul className="text-gray-300 space-y-2">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400"></span>
                    Node.js – Server-side runtime
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400"></span>
                    Express.js – REST API development
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-400"></span>
                    Handles authentication and data flow
                  </li>
                </ul>
              </div>
            </div>

            {/* Database */}
            <div className="group relative p-8 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-orange-500/50 transition-all duration-300 hover:transform hover:-translate-y-1">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-orange-500/0 to-yellow-500/0 group-hover:from-orange-500/5 group-hover:to-yellow-500/5 transition-all duration-300"></div>
              <div className="relative z-10">
                <div className="text-4xl mb-4">🗄️</div>
                <h3 className="text-xl font-bold mb-3 bg-gradient-to-r from-orange-400 to-yellow-400 bg-clip-text text-transparent">
                  Database
                </h3>
                <ul className="text-gray-300 space-y-2">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
                    MongoDB – NoSQL database
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
                    Stores user data and research queries
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-orange-400"></span>
                    Scalable and flexible schema
                  </li>
                </ul>
              </div>
            </div>

            {/* AI Layer */}
            <div className="group relative p-8 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-purple-500/50 transition-all duration-300 hover:transform hover:-translate-y-1">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-purple-500/0 to-pink-500/0 group-hover:from-purple-500/5 group-hover:to-pink-500/5 transition-all duration-300"></div>
              <div className="relative z-10">
                <div className="text-4xl mb-4">🤖</div>
                <h3 className="text-xl font-bold mb-3 bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
                  AI Layer
                </h3>
                <ul className="text-gray-300 space-y-2">
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                    RAG-based pipeline
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                    Embedding & retrieval mechanisms
                  </li>
                  <li className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-purple-400"></span>
                    LLM-powered response generation
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Technology;
