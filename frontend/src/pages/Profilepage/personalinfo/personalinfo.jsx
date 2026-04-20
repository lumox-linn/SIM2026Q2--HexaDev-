import "./Personalinfo.css";
import { useLocation } from "react-router-dom";
function Personalinfo() {
  const location = useLocation();
  const userdata = location.state?.userdata || {};
  console.log(location);
  return <div className="pi">11</div>;
}
export default Personalinfo;
