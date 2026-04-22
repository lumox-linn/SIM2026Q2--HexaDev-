import "../testhead/testheader.css";
import logo from "../../assets/logo.png";
import Navfull from "../navfull/navfull";
import avatar from "../../assets/Avatar.svg";
import ProfileBar from "../profiebar/profillebar";
import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
function Testheader({ onNavClick, Router, user, isVisible, setIsVisible }) {
  console.log(user);
  const location = useLocation();
  const [showpro, setshowpro] = useState(false);
  const [userRavatar, setuserRavatar] = useState(avatar);

  useEffect(() => {
    if (user && user.useravatar !== "null") {
      setuserRavatar(user.useravatar);
    } else {
      setuserRavatar(avatar); // return to default avatar
    }
  }, [user]);
  return (
    <div className="testhead">
      <img
        src={logo}
        alt="Logo"
        className="logo"
        onClick={() => {
          setIsVisible(!isVisible);
        }}
      />
      <Navfull
        Router={Router}
        onLinkClick={onNavClick}
        usre={user}
        className={isVisible ? "active" : ""}
      ></Navfull>
      <ul className="user">
        <li>
          {/* If any user has logged in  */}
          {user ? (
            // if this user has set his avatar then use his, otherwise use default
            <img
              src={userRavatar}
              alt=""
              onClick={() => {
                setshowpro(!showpro);
              }}
            />
          ) : (
            <a href="/login">Login</a>
          )}
        </li>
        {showpro ? (
          <ProfileBar
            user={user}
            key={location.key}
            userRavatar={userRavatar}
          ></ProfileBar>
        ) : (
          ""
        )}
      </ul>
    </div>
  );
}
export default Testheader;
