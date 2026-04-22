import { useEffect, Suspense, useState } from "react";
import {
  useLocation,
  Outlet,
  NavLink,
  useParams,
  useNavigate,
} from "react-router-dom";
import "../profile/profile.css";
import avatar from "../../assets/Avatar.svg";
import logo from "../../assets/logo.png";
console.log(111);
function Profile() {
  console.log("22");
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
  console.log(userdata.role);
  // change link routes
  useEffect(() => {
    if (!userdata) return;
    if (userdata.role === "admin") {
      setlink([
        { to: "ManageAccount", label: "Account Management" },
        { to: "ManageProfile", label: "Profile Management" },
      ]);
    } else if (userdata.role === "Platform manager") {
      setlink([{ to: "ManageActivities", label: "Activity Management" }]);
    } else if (userdata.role === "Donee" || userdata.role === "Fund Raiser") {
      setlink([
        { to: "personalinfo", label: "Profile" },
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
          {/* <div className="headback"></div> */}
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
                {console.log(link)}
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
