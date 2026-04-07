import "../navfull/navfull.css";

function Navfull({
  onLinkClick,
  Router,

  className,
}) {
  return (
    <div className={`navfull ${className || ""}`}>
      <ul>
        <li onClick={() => onLinkClick("search")} style={{ cursor: "pointer" }}>
          Search
        </li>
        <li>
          <a href="/activities">Activities</a>
        </li>
        {Router.filter((item) => item.nav?.title).map((item, idx) => (
          <li key={idx}>
            <a href={item.path}>{item.nav.title}</a>
          </li>
        ))}
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
