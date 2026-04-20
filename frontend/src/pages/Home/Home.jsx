import Header from "../../component/head/header";
import "../Home/home.css";
import Testheader from "../../component/testhead/testheaed";
import Footer from "../../component/footer/footer";
import homebackground from "../../assets/homebackground.jpeg";
import cat from "../../assets/cat2.jpg";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
function Home(props) {
  const location = useLocation();
  const [activeMenu, setActiveMenu] = useState(null);
  const [user, setUser] = useState(() => {
    const savedData = localStorage.getItem("userData");
    if (savedData && savedData !== "undefined") {
      try {
        return JSON.parse(savedData);
      } catch (e) {
        return null;
      }
    }
    return null;
  });
  // controll the state of header
  const [isVisible, setIsVisible] = useState(false);
  const closeMenu = () => setActiveMenu(null);
  const [coverMove, setcoverMove] = useState(false);

  useEffect(() => {
    const updateUserFromStorage = () => {
      const savedData = localStorage.getItem("userData");
      setUser(savedData ? JSON.parse(savedData) : null);
    };
    console.log(user);

    updateUserFromStorage();
    window.addEventListener("storage", updateUserFromStorage);
    // get the sessionstorage data
    const lastPage = sessionStorage.getItem("last_page");

    // see if the user come back from none "/home" path
    if (lastPage) {
      // set navigate to visible
      setIsVisible(true);
      // erase this record, incase it will show neext time
      sessionStorage.removeItem("last_external_page");
    }
    return () => window.removeEventListener("storage", updateUserFromStorage);
  }, []);

  return (
    <div className="home">
      {console.log(user)}
      <Testheader
        Router={props.Router}
        user={user}
        onNavClick={(idx) => setActiveMenu(idx)}
        isVisible={isVisible}
        setIsVisible={setIsVisible}
      ></Testheader>

      <div className="body">
        {/* <img src={homebackground} alt="" className="background" /> */}

        <div className="hometitle">
          <div className="titleleft">
            <span className="cn">HopeLink</span>
            <h2>Every cause deserves a champion and a community</h2>
            <span>
              FundRise connects fundraisers with people who care - for medical
              needs, education, disaster relief, community projects, and more.
            </span>
          </div>
          <div className="titleright">1111</div>
        </div>

        <div className="steps">How FundRise works</div>
        <div className="support">Find a cause to support</div>
        <div className="Built">Built for fundraisers and supporters alike</div>
        <div className="story">Your story can move people. Start today.</div>
        <Footer></Footer>
      </div>

      {activeMenu !== null && (
        <div className="mask">
          <div className="big-box" onClick={(e) => e.stopPropagation()}>
            <i className="x" onClick={closeMenu}>
              X
            </i>
            <div className="searchbar">
              <input type="text" placeholder="Search" className="search" />

              <button
                className="searbutton"
                onClick={(e) => {
                  console.log(e);
                }}
              >
                Search
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
export default Home;
