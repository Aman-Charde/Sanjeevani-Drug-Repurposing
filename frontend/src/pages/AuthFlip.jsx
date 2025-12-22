import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";

const AuthFlip = () => {
  const location = useLocation();
  const [isFlipped, setIsFlipped] = useState(false);

  useEffect(() => {
    setIsFlipped(location.pathname === "/register");
  }, [location.pathname]);

  return (
    <div className="h-screen flex items-center justify-center bg-gray-900">
      <div className="relative w-[950px] h-[620px] perspective">
        <div
          className={`relative w-full h-full transition-transform duration-700 transform-style-preserve-3d ${
            isFlipped ? "rotate-y-180" : ""
          }`}
        >
          <div className="absolute inset-0 backface-hidden">
            <Login />
          </div>

          <div className="absolute inset-0 backface-hidden rotate-y-180">
            <Register />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthFlip;
