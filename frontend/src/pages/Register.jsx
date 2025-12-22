import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import registerImg from "../assets/img.jpg";

const Register = () => {
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const res = await api.post("/auth/register", form);
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("name", res.data.name);
      navigate("/dashboard");
    } catch (err) {
      alert(err.response?.data?.message || "Registration failed");
    }
  };

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div
        className="rounded-[36px] p-[15px] shadow-[0_0_80px_rgba(139,92,246,0.45)]"
        style={{
          background:
            "linear-gradient(310deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%)",
          animation: "float 6s ease-in-out infinite",
        }}
      >
        <div className="relative w-[900px] h-[500px] flex rounded-[28px] overflow-hidden">

          {/* LEFT – IMAGE */}
          <div className="w-1/2 relative">
            <div
              className="absolute inset-0 rounded-r-[300px] bg-cover bg-center"
              style={{ backgroundImage: `url(${registerImg})` }}
            />
          </div>

          {/* RIGHT – FORM */}
          <div className="w-1/2 p-12 text-white">
            <h2 className="text-2xl font-semibold mb-6">
              Create your Account
            </h2>

            <label className="text-sm text-white/70">Full Name</label>
            <input
              className="w-full mt-1 mb-4 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Enter full name"
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />

            <label className="text-sm text-white/70">Email</label>
            <input
              className="w-full mt-1 mb-4 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Enter email"
              onChange={(e) => setForm({ ...form, email: e.target.value })}
            />

            <label className="text-sm text-white/70">Password</label>
            <input
              type="password"
              className="w-full mt-1 mb-6 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Create password"
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />

            <button
              onClick={handleRegister}
              className="w-full py-2 rounded-lg bg-indigo-600 text-white font-semibold
              hover:scale-[1.04] transition hover:shadow-[0_0_25px_rgba(0,212,255,0.9)]"
            >
              Register
            </button>

            <p className="text-sm text-white/70 mt-6 text-center">
              Already have an account?{" "}
              <Link to="/login" className="text-cyan-300 hover:underline">
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
