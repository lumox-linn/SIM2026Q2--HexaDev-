import "./DefaultPage.css";
import { useLocation } from "react-router-dom";
function DefaultPage() {
  const location = useLocation();
  const user = location.state?.userdata;
  console.log(user.role);
  return user.role == "User" ? (
    <div className="dp">
      <li>
        <span>Become a Donee</span>

        <span>Become a Fund Raiser</span>
      </li>
    </div>
  ) : (
    <div>default</div>
  );
}
export default DefaultPage;
