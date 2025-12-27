import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import api from "../services/api";
import loginImg from "../assets/img.jpg";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async () => {
    setIsLoading(true);
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("name", res.data.name);
      navigate("/dashboard");
    } catch (err) {
      alert(err.response?.data?.message || "Invalid credentials");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    setIsLoading(true);
    try {
      const res = await api.post("/auth/google", {
        credential: credentialResponse.credential
      });
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("name", res.data.name);
      navigate("/dashboard");
    } catch (err) {
      alert(err.response?.data?.message || "Google sign-in failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleError = () => {
    alert("Google Sign-In failed. Please try again.");
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
        <div className="relative w-[900px] h-[580px] flex rounded-[28px] overflow-hidden">

          {/* LEFT – FORM */}
          <div className="w-1/2 p-10 text-white overflow-y-auto">
            <h2 className="text-2xl font-semibold mb-5">
              Sign in to your Account
            </h2>

            <label className="text-sm text-white/70">Email</label>
            <input
              className="w-full mt-1 mb-3 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Enter email"
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
            />

            <label className="text-sm text-white/70">Password</label>
            <input
              type="password"
              className="w-full mt-1 mb-4 px-4 py-2 rounded-lg
              bg-white/20 border border-white/60 text-white
              placeholder:text-white/50 focus:ring-2 focus:ring-cyan-400"
              placeholder="Enter password"
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
            />

            <div className="flex justify-between items-center text-sm mb-4">
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
              disabled={isLoading}
              className="w-full py-2 rounded-lg bg-indigo-600 text-white font-semibold
              hover:scale-[1.04] transition hover:shadow-[0_0_25px_rgba(0,212,255,0.9)]
              disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
            >
              {isLoading ? "Signing in..." : "Sign In"}
            </button>

            {/* Divider */}
            <div className="flex items-center my-4">
              <div className="flex-1 h-px bg-white/30"></div>
              <span className="px-4 text-sm text-white/50">or continue with</span>
              <div className="flex-1 h-px bg-white/30"></div>
            </div>

            {/* Google Sign-In Button */}
            <div className="flex justify-center">
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={handleGoogleError}
                theme="filled_black"
                size="large"
                width="320"
                text="signin_with"
                shape="rectangular"
                logo_alignment="left"
              />
            </div>

            <p className="text-sm text-white/70 mt-5 text-center">
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
