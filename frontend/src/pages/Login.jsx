import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import loginImg from "../assets/img.jpg";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("name", res.data.name);
      navigate("/dashboard");
    } catch {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="w-full h-full flex items-center justify-center">
      {/* 🌈 OUTER BORDER (NO backdrop blur) */}
      <div
        className="rounded-[36px] p-[15px] shadow-[0_0_80px_rgba(139,92,246,0.45)]"
        style={{
          background:
            "linear-gradient(145deg, rgba(2,0,36,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%)",
          animation: "float 6s ease-in-out infinite",
        }}
      >
        {/* 🧊 INNER CARD */}
        <div className="relative w-[900px] h-[500px] flex rounded-[28px] overflow-hidden">

          {/* LEFT – FORM */}
          <div className="w-1/2 p-12 text-white">
            <h2 className="text-2xl font-semibold mb-6">
              Sign in to your Account
            </h2>

            <label className="text-sm text-white/70">Email</label>
            <input
              className="w-full mt-1 mb-4 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Enter email"
              onChange={(e) => setEmail(e.target.value)}
            />

            <label className="text-sm text-white/70">Password</label>
            <input
              type="password"
              className="w-full mt-1 mb-6 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Enter password"
              onChange={(e) => setPassword(e.target.value)}
            />

            <div className="flex justify-between items-center text-sm mb-5">
              <label className="flex items-center gap-2 text-white/70">
                <input type="checkbox" />
                Remember me
              </label>
              <span className="text-cyan-300 cursor-pointer">
                Forgot password?
              </span>
            </div>

            <button
              onClick={handleLogin}
              className="w-full py-2 rounded-lg bg-indigo-600 text-white font-semibold
              hover:scale-[1.04] transition hover:shadow-[0_0_25px_rgba(0,212,255,0.9)]"
            >
              Sign In
            </button>

            <p className="text-sm text-white/70 mt-6 text-center">
              Not registered yet?{" "}
              <Link to="/register" className="text-cyan-300 hover:underline">
                Create an account
              </Link>
            </p>
          </div>

          {/* RIGHT – IMAGE */}
          <div className="w-1/2 relative">
            <div
              className="absolute inset-0 rounded-l-[300px] bg-cover bg-center"
              style={{ backgroundImage: `url(${loginImg})` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
