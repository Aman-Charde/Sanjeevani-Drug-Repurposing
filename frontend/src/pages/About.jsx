import React from 'react'
import { Link } from 'react-router-dom';
import ChromaGrid from '../components/reactbits/ChromaGrid/ChromaGrid'
import AmanImg from '../assets/AmanTeamMember.png'
import AnshImg from '../assets/AnshTeamMember.png'

const About = () => {
  const items = [
    {
      image: AmanImg,
      title: "Aman Charde",
      subtitle: "Full Stack Developer",
      handle: "@amancharde",
      borderColor: "#09C8BE",
      gradient: "linear-gradient(145deg, #27F5EB, #000)",
      url: "https://github.com/aman-charde"
    },
    {
      image: AnshImg,
      title: "Ansh Sable",
      subtitle: "AIML Engineer",
      handle: "@anshsable",
      borderColor: "#00befeff",
      gradient: "linear-gradient(180deg, #004782ff, #000)",
      url: "https://linkedin.com/in/anshsable"
    }
  ];
  // Features for What We Do section
  const features = [
    {
      icon: "🧬",
      title: "AI-Powered Analysis",
      description: "Leveraging cutting-edge machine learning algorithms to analyze complex molecular structures and predict drug interactions.",
      gradient: "from-blue-500 to-cyan-400"
    },
    {
      icon: "💊",
      title: "Drug Repurposing",
      description: "Finding new therapeutic applications for existing FDA-approved drugs, dramatically reducing development time and costs.",
      gradient: "from-purple-500 to-pink-400"
    },
    {
      icon: "📊",
      title: "Biomedical Data",
      description: "Processing vast amounts of biomedical literature and clinical data to uncover hidden patterns and opportunities.",
      gradient: "from-orange-500 to-yellow-400"
    }
  ];

  return (
    <div className="min-h-screen bg-[#050816] text-white">
      {/* Meet Our Team Section */}
      <section className="relative px-6 py-20 md:px-10 lg:px-20">
        {/* Back Button */}
        <Link
          to="/"
          className="absolute top-6 left-6 md:left-10 z-20 group flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 hover:border-pink-500/50 transition-all duration-300"
        >
          <span className="text-lg group-hover:-translate-x-1 transition-transform duration-300">←</span>
          <span className="text-sm font-medium text-gray-300 group-hover:text-white transition-colors duration-300">Back to Home</span>
        </Link>

        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <span className="text-sm font-semibold text-pink-400 uppercase tracking-wider">The People</span>
            <h2 className="text-4xl md:text-5xl font-bold mt-2 mb-4 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              Meet Our Team
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              The brilliant minds behind Sanjeevani working to revolutionize drug discovery
            </p>
          </div>

          <div style={{ height: '550px', position: 'relative' }}>
            <ChromaGrid
              items={items}
              columns={2}
              rows={1}
              radius={300}
              damping={0.45}
              fadeOut={0.6}
              ease="power3.out"
            />
          </div>
        </div>
      </section>
    </div>
  )
}

export default About;