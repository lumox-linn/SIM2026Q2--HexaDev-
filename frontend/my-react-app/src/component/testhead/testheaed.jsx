import "../testhead/testheader.css";
import logo from "../../assets/logo.svg";
import Navfull from "../navfull/navfull";
import avatar from "../../assets/Avatar.svg";
import ProfileBar from "../profiebar/profillebar";
import Navigationr from "../navigationr/Navigationr";
import Navigationl from "../navigationl/navigationl";
import { useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
function Testheader({ onNavClick, Router, user, isVisible, setIsVisible }) {
  const location = useLocation();
  const [showpro, setshowpro] = useState(false);
  const [userRavatar, setuserRavatar] = useState(avatar);
  const currentAvatar = location.state?.userRavatar;

  useEffect(() => {
    // if avatar is in the state, store into the sessionstorage
    if (currentAvatar) {
      sessionStorage.setItem("user_avatar_cache", currentAvatar);
    }
  }, [currentAvatar]);
  const finalAvatar =
    currentAvatar || sessionStorage.getItem("user_avatar_cache") || avatar;
  console.log(user);
  useEffect(() => {
    console.log(avatar);

    if (user && user.useravatar !== null) {
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
          {console.log(user)}
          {user ? (
            // if this user has set his avatar then use his, otherwise use default
            <img
              src={finalAvatar}
              alt=""
              onClick={() => {
                setshowpro(!showpro);
              }}
            />
          ) : (
            <a href="/login" onClick={() => clear}>
              Login
            </a>
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
