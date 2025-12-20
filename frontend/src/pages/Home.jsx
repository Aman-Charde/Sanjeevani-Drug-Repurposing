import Navbar from "../components/Navbar";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-200">
      <Navbar />

      <div className="flex flex-col items-center justify-center text-center px-4 mt-32">
        <h1 className="text-4xl font-bold mb-4">
          Sanjeevani
        </h1>

        <p className="max-w-xl text-gray-400">
          An AI-Based Drug Repurposing System that assists researchers
          in discovering potential new uses of existing drugs.
        </p>
      </div>
    </div>
  );
};

export default Home;
