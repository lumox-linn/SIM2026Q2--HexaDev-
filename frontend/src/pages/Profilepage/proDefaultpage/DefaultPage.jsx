import "./DefaultPage.css";
import { useLocation, Navigate } from "react-router-dom";
function DefaultPage() {
  const location = useLocation();
  const user = location.state?.userdata;
  console.log(location);
  if (!user || user.role !== "fundraiser") {
    return <Navigate to="MyDonations" replace />;
  }
  // 3. 只有是 fundraiser 的时候，才会看到下面的真实内容
  return (
    <div className="fundraiser-default-dashboard">
      <h2>Welcome, Fundraiser!</h2>
      {/* 你的筹款人专属看板内容 */}
    </div>
  );
}
export default DefaultPage;
