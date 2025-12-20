import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center px-8 py-4 border-b border-gray-800">
      <h1 className="text-xl font-bold text-white">
        Sanjeevani
      </h1>

      <Link to="/login">
        <button className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md">
          Sign In
        </button>
      </Link>
    </nav>
  );
};

export default Navbar;
