import "../head/header.css";
import logo from "../../assets/logo.svg";

import Navigationr from "../navigationr/Navigationr";
import Navigationl from "../navigationl/navigationl";
import { useEffect, useState } from "react";
function Header({ onNavClick, Router, user, isVisible, setIsVisible }) {
  // const [isVisible, setIsVisible] = useState(false);
  useEffect(() => {
    console.log("Router in Header:", Router);
  }, [Router]);
  console.log(user);
  return (
    <div className="head">
      <Navigationl
        Router={Router}
        onLinkClick={onNavClick}
        className={isVisible ? "active" : ""}
      ></Navigationl>
      <img
        src={logo}
        alt="Logo"
        className="logo"
        onClick={() => {
          setIsVisible(!isVisible);
        }}
      />
      <Navigationr
        Router={Router}
        user={user}
        className={isVisible ? "active" : ""}
        userstatus
        state
      ></Navigationr>
    </div>
  );
}
export default Header;
