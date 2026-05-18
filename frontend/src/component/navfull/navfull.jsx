import "../navfull/navfull.css";
import RouterConfig from "../../router/Router";
import { Link } from "react-router-dom";
function Navfull({
  onLinkClick,

  className,
}) {
  const location = useLocation();
  const userdata = location.state?.userdata || {};
  console.log(userdata);
  return (
    <div className={`navfull ${className || ""}`}>
      <ul>
        11
        {/* <li onClick={() => onLinkClick("search")} style={{ cursor: "pointer" }}>
          Search
        </li> */}
        {console.log(userdata)}
        {userdata.role == "donee" ? (
          <li>
            <a href="/activities">Activities</a>
          </li>
        ) : null}
        {/* {RouterConfig.filter((item) => item.nav?.title).map((item, idx) => (
          <li key={idx}>
            <a href={item.path}>{item.nav.title}</a>
          </li>
        ))} */}
      </ul>

      {/* <ul>
        <li className="user">
          {/* If any user has logged in  */}
      {/* {user ? (
            // if this user has set his avatar then use his, otherwise use default
            <img src={user.useravatar ? user.useravatar : avatar} alt="" />
          ) : (
            <a href="/login">Login</a>
          )} */}
      {/* </li> */}
      {/* </ul> */}
    </div>
  );
}
export default Navfull;
