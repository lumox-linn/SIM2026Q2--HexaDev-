import { useEffect, useState } from "react";
// import Router from "../../router/Router";
import avatar from "../../assets/Avatar.svg";
import ProfileBar from "../profiebar/profillebar";
import "./Navigationr.css";
function Navigationr({ Router = [], className, user }) {
  const [showpro, setshowpro] = useState(false);
  useEffect(() => {
    console.log(user);
  });

  return (
    <div className={`navr ${className || ""}`}>
      <ul>
        {Router.filter((item) => item.nav?.title).map((item, idx) => (
          <li key={idx}>
            <a href={item.path}>{item.nav.title}</a>
          </li>
        ))}
        <li className="user">
          {/* If any user has logged in  */}
          {user ? (
            // if this user has set his avatar then use his, otherwise use default
            <img
              src={user.useravatar ? user.useravatar : avatar}
              alt=""
              onClick={() => {
                setshowpro(!showpro);
              }}
            />
          ) : (
            <a href="/login">Login</a>
          )}
        </li>
      </ul>
      {showpro ? <ProfileBar user={user}></ProfileBar> : ""}
    </div>
  );
}
export default Navigationr;
