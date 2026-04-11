import "../profiebar/profilebar.css";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import arrow from "../../assets/arrow.svg";
import { apiLogout } from "../../api";
function ProfileBar({ user, userRavatar }) {
  console.log(user, userRavatar);
  const navigate = useNavigate();

  // if avatar is in the state, store into the sessionstorage
  // if (currentAvatar) {
  //   sessionStorage.setItem("user_avatar_cache", currentAvatar);
  // }

  console.log(user);
  const logout = async (userid) => {
    console.log(userid);
    try {
      const res = await apiLogout(userid);
      if (res.userdata.loginstatus == false) {
        sessionStorage.setItem(
          "login_status",
          JSON.stringify(res.userdata.loginstatus),
        );
      }
      console.log(res);
    } catch (error) {}
  };
  if (!user) return null;
  return (
    <div className="ProfileBar">
      <img src={arrow} alt="" className="arrow" />
      <div className="userinfo">
        <li>
          {/* <img src="" alt="" /> */}
          {user.username}
        </li>
        <li className="email">{user.email}</li>
      </div>
      <ul>
        <li
          onClick={() =>
            navigate(`/profile/${user.userid}`, {
              state: { userdata: user, userRavatar: userRavatar },
            })
          }
        >
          Profile
        </li>
        <li>history</li>
        <li
          onClick={() => {
            logout(user.userid);
            localStorage.removeItem("userData");
            window.dispatchEvent(new Event("storage"));

            navigate("/home");
          }}
        >
          Logout
        </li>
      </ul>
    </div>
  );
}
export default ProfileBar;
