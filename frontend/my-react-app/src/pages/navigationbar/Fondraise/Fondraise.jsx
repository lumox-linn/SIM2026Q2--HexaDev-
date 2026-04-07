import { Navigate, useNavigate } from "react-router-dom";

function Fondraise() {
  const navigate = useNavigate();
  return (
    <div>
      <span onClick={() => navigate("/home", { state: { fromOutside: true } })}>
        fondraise
      </span>
    </div>
  );
}
export default Fondraise;
