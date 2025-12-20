const Dashboard = () => {
  const name = localStorage.getItem("name");

  const logout = () => {
    localStorage.clear();
    window.location.href = "/login";
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-200 p-8">
      
      {/* Top Bar */}
      <div className="flex justify-between items-center mb-10">
        <h1 className="text-2xl font-bold">
          Sanjeevani Dashboard
        </h1>

        <div className="flex items-center gap-4">
          <span className="text-gray-400">
            Hi, {name}
          </span>
          <button
            onClick={logout}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 rounded"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Intro Section */}
      <div className="bg-gray-800 p-6 rounded-lg mb-10">
        <h2 className="text-xl font-semibold mb-2">
          Welcome to Sanjeevani
        </h2>
        <p className="text-gray-400">
          Sanjeevani is an AI-Based Drug Repurposing System designed to
          help researchers explore potential new uses of existing drugs.
          This platform provides AI-powered insights based on biomedical
          research data.
        </p>
      </div>

      {/* Action Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <div className="bg-gray-800 p-6 rounded-lg hover:border hover:border-indigo-500 transition">
          <h3 className="text-lg font-semibold mb-2">
            New Drug Repurposing Query
          </h3>
          <p className="text-gray-400 mb-4">
            Submit a new disease-based query to get AI-generated insights.
          </p>
          <button className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded">
            Start New Query
          </button>
        </div>

        <div className="bg-gray-800 p-6 rounded-lg hover:border hover:border-indigo-500 transition">
          <h3 className="text-lg font-semibold mb-2">
            Query History
          </h3>
          <p className="text-gray-400 mb-4">
            View and manage your previously submitted queries.
          </p>
          <button className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded">
            View History
          </button>
        </div>

      </div>
    </div>
  );
};

export default Dashboard;
