import { useEffect, Suspense, useState } from "react";
import {
  useLocation,
  Outlet,
  NavLink,
  useParams,
  useNavigate,
} from "react-router-dom";
import "../profile/profile.css";
import Router from "../../router/Router";
import avatar from "../../assets/Avatar.svg";
import logo from "../../assets/logo.svg";
import headback from "../../assets/headback.svg";
function Profile() {
  const { id } = useParams();
  const location = useLocation();
  const userdata = location.state?.userdata || {};
  const currentAvatar = location.state?.userRavatar;
  const navigate = useNavigate();
  const lastPage = sessionStorage.getItem("last_page");
  const [link, setlink] = useState([
    { to: "ManageAccount", label: "Manage Account" },
  ]);
  useEffect(() => {
    // if avatar is in the state, store into the sessionstorage
    if (currentAvatar) {
      sessionStorage.setItem("user_avatar_cache", currentAvatar);
    }
  }, [currentAvatar]);
  // change link routes
  useEffect(() => {
    if (!userdata) return;
    if (userdata.role === "Admin") {
      setlink([{ to: "ManageAccount", label: "User Management" }]);
    } else if (userdata.role === "Platform manager") {
      setlink([{ to: "ManageActivities", label: "Activity Management" }]);
    } else if (userdata.role === "User") {
      setlink([
        { to: "personalinfo", label: "Personal Info" },
        { to: "ActivityStatus", label: "Activity Status" },
      ]);
    }
  }, [userdata]);
  const finalAvatar =
    currentAvatar || sessionStorage.getItem("user_avatar_cache") || avatar;
  return (
    <div className="profile">
      <div className="usernav">
        <img
          src={logo}
          alt=""
          className="logo"
          onClick={() => navigate("/home")}
        />
        <ul className="userhead">
          {/* <img src={headback} alt="" className="headback" /> */}
          <div className="headback"></div>
          <li className="ava">
            <img src={finalAvatar} alt="" />
          </li>
          <li className="role">
            <span>{userdata?.username}</span>
            <span>{userdata?.role}</span>
          </li>
        </ul>
        <ul className="userbody">
          {link.map((links) => (
            <li key={links.to}>
              <NavLink
                to={`/profile/${id}/${links.to}`}
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
                state={{
                  userdata: userdata,
                  userRavatar: finalAvatar,
                }}
              >
                {links.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
      <div className="proshow">
        <Suspense fallback={<div>Loading...</div>}>
          <Outlet />
        </Suspense>
      </div>
    </div>
  );
}
export default Profile;
