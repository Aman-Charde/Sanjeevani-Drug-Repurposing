import { Link } from 'react-router-dom';

const About1 = () => {
  return (
    <div className="min-h-screen bg-[#050816] text-white">
      {/* Hero Section */}
      <section className="relative px-6 py-20 md:px-10 lg:px-20 overflow-hidden">
        {/* Back Button */}
        <Link
          to="/"
          className="absolute top-6 left-6 md:left-10 z-20 group flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-purple-500/50 transition-all duration-300"
        >
          <span className="text-lg group-hover:-translate-x-1 transition-transform duration-300">←</span>
          <span className="text-sm font-medium text-gray-300 group-hover:text-white transition-colors duration-300">Back to Home</span>
        </Link>

        {/* Background decorative elements */}
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-10 right-10 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>

        <div className="relative z-10 max-w-6xl mx-auto text-center">
          <span className="text-sm font-semibold text-purple-400 uppercase tracking-wider">About Us</span>
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mt-4 mb-6 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
            About <span className="bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">Sanjeevani</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
            Sanjeevani is an AI-powered drug repurposing system designed to
            identify new therapeutic uses for existing approved drugs using
            machine learning and biomedical data analysis.
          </p>
        </div>
      </section>

      {/* What We Do Section */}
      <section className="px-6 py-16 md:px-10 lg:px-20">
        <div className="max-w-6xl mx-auto">
          <div className="group relative p-8 md:p-10 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-purple-500/50 transition-all duration-300">
            {/* Glow effect on hover */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-purple-500/0 to-pink-500/0 group-hover:from-purple-500/5 group-hover:to-pink-500/5 transition-all duration-300"></div>

            <div className="relative z-10">
              <span className="text-sm font-semibold text-blue-400 uppercase tracking-wider">Our Mission</span>
              <h2 className="text-3xl md:text-4xl font-bold mt-2 mb-6 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                What We Do
              </h2>
              <p className="text-gray-300 leading-relaxed text-lg mb-4">
                Sanjeevani analyzes existing drug and disease data to predict
                potential new applications of approved drugs. By leveraging
                artificial intelligence and machine learning techniques, the
                system identifies hidden patterns and similarities between drugs
                and diseases.
              </p>
              <p className="text-gray-300 leading-relaxed text-lg">
                Our platform provides ranked drug recommendations along with
                confidence scores, helping researchers explore faster and
                cost-effective treatment possibilities.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Problem We Solve Section */}
      <section className="px-6 py-16 md:px-10 lg:px-20">
        <div className="max-w-6xl mx-auto">
          <div className="group relative p-8 md:p-10 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-orange-500/50 transition-all duration-300">
            {/* Glow effect on hover */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-orange-500/0 to-yellow-500/0 group-hover:from-orange-500/5 group-hover:to-yellow-500/5 transition-all duration-300"></div>

            <div className="relative z-10">
              <span className="text-sm font-semibold text-orange-400 uppercase tracking-wider">The Challenge</span>
              <h2 className="text-3xl md:text-4xl font-bold mt-2 mb-6 bg-gradient-to-r from-orange-400 to-yellow-400 bg-clip-text text-transparent">
                Problem We Solve
              </h2>
              <p className="text-gray-300 leading-relaxed text-lg mb-4">
                Traditional drug discovery is extremely time-consuming, expensive,
                and risky. Developing a new drug can take over a decade and cost
                billions of dollars, with a high failure rate.
              </p>
              <p className="text-gray-300 leading-relaxed text-lg">
                Additionally, in emergency situations such as pandemics or rare
                diseases, there is often not enough time to develop new drugs from
                scratch. Sanjeevani addresses this challenge by reusing existing,
                clinically tested drugs for new diseases.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Why Drug Repurposing Section */}
      <section className="px-6 py-16 md:px-10 lg:px-20">
        <div className="max-w-6xl mx-auto">
          <div className="group relative p-8 md:p-10 rounded-2xl bg-gradient-to-b from-gray-800/50 to-gray-900/50 border border-gray-700/50 hover:border-green-500/50 transition-all duration-300">
            {/* Glow effect on hover */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-green-500/0 to-emerald-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>

            <div className="relative z-10">
              <span className="text-sm font-semibold text-green-400 uppercase tracking-wider">The Solution</span>
              <h2 className="text-3xl md:text-4xl font-bold mt-2 mb-6 bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                Why Drug Repurposing
              </h2>
              <p className="text-gray-300 leading-relaxed text-lg mb-6">
                Drug repurposing offers a faster and safer alternative to
                traditional drug development. Since repurposed drugs are already
                approved or clinically tested, their safety profiles are well
                understood.
              </p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">⚡</span>
                  <span className="text-gray-300">Reduces drug development time and cost</span>
                </li>
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">🛡️</span>
                  <span className="text-gray-300">Minimizes clinical risk</span>
                </li>
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">🚀</span>
                  <span className="text-gray-300">Enables rapid response to emerging diseases</span>
                </li>
                <li className="flex items-center gap-3 p-4 rounded-xl bg-white/5 border border-white/10">
                  <span className="text-2xl">🧠</span>
                  <span className="text-gray-300">Leverages existing biomedical knowledge</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer Section */}
      <section className="px-6 py-16 md:px-10 lg:px-20 border-t border-gray-800">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-start gap-4 p-6 rounded-xl bg-yellow-500/5 border border-yellow-500/20">
            <span className="text-3xl">⚠️</span>
            <div>
              <h3 className="text-lg font-semibold text-yellow-400 mb-2">Disclaimer</h3>
              <p className="text-gray-400">
                Sanjeevani is developed for research and educational
                purposes only and is not intended for direct clinical or medical use.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About1;
