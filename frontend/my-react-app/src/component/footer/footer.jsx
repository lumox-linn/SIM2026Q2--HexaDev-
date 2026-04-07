import "../footer/footer.css";
import x from "../../assets/x_twiter.svg";
import youtube from "../../assets/youtube.svg";
import instagram from "../../assets/instagram.svg";
function Footer() {
  return (
    <div className="footer">
      <li className="about">
        <a href="/donate">Donate</a>
        <a href="/about">About</a>
        <a href="/fundraise">Fondraise</a>
        {/* <a href=""></a> */}
      </li>
      <hr />
      <li>Email:</li>
      <li>Phone:</li>
      <li>
        <img src={x} alt="" />
        <img src={youtube} alt="" />
        <img src={instagram} alt="" />
      </li>
    </div>
  );
}
export default Footer;
