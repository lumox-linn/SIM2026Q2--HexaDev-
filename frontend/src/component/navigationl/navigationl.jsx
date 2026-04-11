import "../navigationl/navigationl.css";
function Navigationl({ onLinkClick, Router = [], className }) {
  return (
    <div className={`navl ${className || ""}`}>
      <ul>
        <li onClick={() => onLinkClick("search")} style={{ cursor: "pointer" }}>
          Search
        </li>
        <li>
          <a href="/activities">Activities</a>
        </li>
        <li>
          <span>pppp</span>
        </li>
      </ul>
    </div>
  );
}
export default Navigationl;
