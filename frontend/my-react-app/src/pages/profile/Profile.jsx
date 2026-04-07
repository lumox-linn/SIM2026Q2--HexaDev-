import { useEffect, Suspense } from "react";
import { useLocation, Outlet, Link, useParams } from "react-router-dom";
import "../profile/profile.css";
import Router from "../../router/Router";
import avatar from "../../assets/Avatar.svg";
import logo from "../../assets/logo.svg";
function Profile() {
  const { id } = useParams();
  const location = useLocation();
  const userdata = location.state?.userdata;
  const currentAvatar = location.state?.userRavatar;

  useEffect(() => {
    // if avatar is in the state, store into the sessionstorage
    if (currentAvatar) {
      sessionStorage.setItem("user_avatar_cache", currentAvatar);
    }
  }, [currentAvatar]);
  const finalAvatar =
    currentAvatar || sessionStorage.getItem("user_avatar_cache") || avatar;
  return (
    <div className="profile">
      <div className="usernav">
        <img src={logo} alt="" className="logo" />
        <ul className="userhead">
          <li>
            <img src={finalAvatar} alt="" />
          </li>
          <li className="role">
            <span>{userdata?.username}</span>
            <span>{userdata?.role}</span>
          </li>
        </ul>
        <ul className="userbody">
          <li>
            <Link
              to={`/profile/${id}/personalinfo`}
              className="nav-link"
              state={{
                userdata: userdata,
              }}
            >
              Personal Info
            </Link>
          </li>
          <li>
            <Link
              to={`/profile/${id}/myactivities`}
              className="nav-link"
              state={{
                userdata: userdata,
              }}
            >
              My Activities
            </Link>
          </li>
        </ul>
      </div>
      <div className="proshow">
        <Outlet />
      </div>
    </div>
  );
}
export default Profile;
