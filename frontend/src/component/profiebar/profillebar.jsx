import "../profiebar/profilebar.css";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import arrow from "../../assets/arrow.svg";
import { apiLogout } from "../../api";
function ProfileBar({ user, userRavatar }) {
  console.log(user);
  const navigate = useNavigate();
  const logout = async (userid) => {
    console.log(userid);
    try {
      const res = await apiLogout({ userid: userid });
      if (res.userdata.loginstatus == false) {
        sessionStorage.setItem(
          "login_status",
          JSON.stringify(res.userdata.loginstatus),
        );
      }
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
          Manage your account
        </li>
        <li>Saved</li>
        <li
          onClick={() => {
            logout(user.userid);
            // remove the localstorage
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
