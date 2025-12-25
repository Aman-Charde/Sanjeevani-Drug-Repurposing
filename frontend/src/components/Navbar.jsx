import CardNav from "./reactbits/CardNav/CardNav";
import logo from "../assets/loogoo.png";

export default function Navbar({
  items,
  baseColor = "#242424",
  menuColor = "#ffffff",
  buttonBgColor = "#5227FF",
  buttonTextColor = "#ffffff",
  isLoggedIn = false,
  onLogout
}) {
  return (
    <div className="relative z-50">
      <CardNav
        logo={logo}
        logoAlt="Sanjeevani Logo"
        items={items}
        baseColor={baseColor}
        menuColor={menuColor}
        buttonBgColor={buttonBgColor}
        buttonTextColor={buttonTextColor}
        ease="power3.out"
        isLoggedIn={isLoggedIn}
        onLogout={onLogout}
      />
    </div>
  );
}
