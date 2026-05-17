import "./ManageActivities.css";
import { useLocation } from "react-router-dom";
import cookie from "js-cookie";
import { useState, useEffect } from "react";
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";
import { createStaticStyles } from "antd-style";
import {
  Button,
  Checkbox,
  Form,
  Input,
  message,
  Modal,
  Flex,
  DatePicker,
  Space,
  Tag,
  Progress,
  Select,
} from "antd";
import { apiRemoveFavorites, apiGetAllFavorites } from "../../api";
function Favorites() {
  const location = useLocation();
  const [selectedActivities, setselectedActivities] = useState(null);
  const userdata = location.state?.userdata || {};
  const [isModalOpen, setIsModalOpen] = useState(false);
  const currentAvatar = location.state?.userRavatar;
  console.log(userdata, currentAvatar);
  const [activityData, setactivityData] = useState([]);
  const [viewActivity, setViewActivity] = useState({
    viewstatus: false,
    actId: null,
  });
  const getStatusClass = (item) => {
    if (item.status === "suspended") return "disabled";
    return "active";
  };
  const [targetNumber, settargetNumber] = useState(false);
  const percentage = (item) => {
    const raised = parseFloat(item.amount_raised) || 0;
    const target = parseFloat(item.target_amount) || 0;
    if (target <= 0) return 0;
    const res = Math.round((raised / target) * 100);

    return res;
  };
  useEffect(() => {
    refresh();
  }, []);
  // total favoraite count
  const totalF = 0;
  const handleOk = () => {
    setIsModalOpen(false);
    if (!selectedActivities) return;
    console.log(selectedActivities);
    // try {
    //   apiRemoveFavorites(selectedActivities.activity_id)
    //     .then((res) => {
    //       console.log(res);
    //       if (res.status === "success") {
    //         message.success(res.message);
    //         refresh();
    //       } else {
    //         message.error(res.error || "Failed to delete");
    //       }
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //       message.error(err.response?.data?.error);
    //     });
    // } catch (error) {
    //   console.log(error);
    //   message.error(error.response?.data?.error);
    // }
  };
  const stylesFn = (info) => {
    const val = info.props.percent ?? 0;
    const safeVal = Math.min(Math.max(val, 0), 100);
    const hue = 200 - (200 * val) / 100;
    return {
      indicator: {
        backgroundImage: `
        linear-gradient(
          to right,
          hsla(${hue}, 85%, 65%, 1),
          height: '8px',
          hsla(${hue + 30}, 90%, 55%, 0.95)
        )`,
        borderRadius: 8,
        transition: "all 0.3s ease",
      },
      rail: {
        backgroundColor: "rgba(0, 0, 0, 0.1)",
        borderRadius: 8,
        height: "8px",
      },
    };
  };
  const progressClass = {
    root: "demo-progress-root",
    rail: "demo-progress-rail",
    track: "demo-progress-track",
  };
  const styles = {
    root: {
      backgroundColor: "#e6f7ff",
    },
    icon: {
      color: "#52c41a",
    },
    content: {
      color: "#706d6d",
    },
  };
  const showModal = (profile) => {
    setselectedActivities(profile);
    setIsModalOpen(true);
  };
  const refresh = () => {
    const token = cookie.get("token");
    console.log(activityData);
    try {
      apiGetAllFavorites({ user_id: userdata.userid }, token)
        .then((res) => {
          console.log(res);
          if (res.activities) {
            const activities = res.activities.map((item) => ({
              activity_id: item.activity_id,
              title: item.title,
              description: item.description,
              amount_raised: item.amount_raised,
              category_name: item.category_name,
              status: item.status,
              creator: item.creator,
              target_amount: item.target_amount,
              category_id: item.category_id,
              start_date: item.start_date,
              // start_date: item.start_date.split(" ").slice(0, 4).join(" "),
              end_date: item.end_date,
            }));
            setactivityData(activities);
          }
        })
        .catch((err) => {
          console.log(err);
          // message.error(err.response?.data?.error);
        });
    } catch (error) {
      console.log(error);
      // message.error(error.response?.data?.error);
    }
  };

  const classNames = createStaticStyles(({ css }) => ({
    root: css`
      padding: 2px 6px;
      border-radius: 8px;
      margin-left: 10px;
    `,
  }));
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  const viewAct = (item) => {
    setViewActivity({
      viewstatus: true,
      actId: item.activity_id,
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="mac">
      <div className="top">
        <img src={currentAvatar} alt="" />
        <li>{userdata.role}</li>
        <li>Total favorites: {totalF}</li>
      </div>
      <div className="flist">
        <li className="search">
          <input type="text" placeholder="Enter Category" />
          <button>Search</button>
        </li>
        <div className="list">
          {activityData
            .slice()
            .sort((a, b) => {
              if (a.activity_id === viewActivity.actId) return -1;
              if (b.activity_id === viewActivity.actId) return 1;
              return 0;
            })
            .map((item) => {
              return (
                <div
                  key={item.activity_id}
                  className={
                    item.activity_id === viewActivity.actId
                      ? "cardView"
                      : "card"
                  }
                >
                  {item.activity_id === viewActivity.actId ? (
                    <i
                      onClick={() =>
                        setViewActivity({ actId: null, viewstatus: false })
                      }
                      className="closeView"
                    >
                      X
                    </i>
                  ) : (
                    ""
                  )}

                  <li className="first">
                    <span className="name">{item.title}</span>

                    <div className={getStatusClass(item)}>
                      {item.status === "active" ? "Active" : "Suspended"}
                    </div>
                    {item.activity_id === viewActivity.actId ? (
                      <p>
                        <Tag
                          classNames={classNames}
                          styles={styles}
                          icon={
                            item.status === "active" ? (
                              <CheckCircleOutlined />
                            ) : (
                              <CloseCircleOutlined />
                            )
                          }
                        >
                          {item.category_name}
                        </Tag>
                      </p>
                    ) : null}
                    <button
                      onClick={() => setselectedActivities(item)}
                      style={{
                        position: "absolute",
                        right: "2px",
                        top: "10px",
                        width: "60px",
                      }}
                    >
                      Remove
                    </button>
                  </li>
                  {item.activity_id === viewActivity.actId ? (
                    <li className="date">
                      <p>
                        <span>Start date: {item.start_date}</span>
                        <span style={{ marginLeft: "30px", color: "#eb2f2f" }}>
                          End date: {item.end_date}
                        </span>
                      </p>

                      <p
                        style={{
                          width: "100%",
                          height: "20px",
                          display: "flex",
                          flexDirection: "row",
                          // padding: "0 2px",
                          justifyContent: "space-between",
                        }}
                      >
                        {" "}
                        <span style={{ color: "#6bacea" }}>
                          Target: ${item.target_amount}
                        </span>
                        <span style={{ color: "#b3bc4b" }}>
                          Raised: ${item.amount_raised}
                        </span>
                      </p>
                      <Flex vertical gap="large">
                        {/* <span>{item.targetAmount}</span> */}
                        <Progress
                          classNames={progressClass}
                          styles={stylesFn}
                          percent={percentage(item)}
                        />
                      </Flex>
                      {/* <hr /> */}
                    </li>
                  ) : null}

                  <span style={{ marginBottom: "45px" }}>
                    {item.description}
                  </span>

                  <li
                    className="butStyle"
                    style={{
                      position: "absolute",
                      bottom: "13px",
                      zIndex: 10,
                      left: "19px",
                    }}
                  >
                    <button>Donate</button>

                    {viewActivity.actId == item.activity_id ? null : (
                      <button
                        onClick={() => {
                          viewAct(item);
                        }}
                      >
                        View
                      </button>
                    )}

                    {/* <Modal
                      title="Remove confirmation"
                      open={isModalOpen}
                      onOk={handleOk}
                      onCancel={handleCancel}
                      okText="Remove"
                      okType="danger"
                      className="modall"
                    >
                      <p>
                        Are you sure you want to remove this List
                        <b> {selectedActivities?.title}?</b>
                      </p>
                    </Modal> */}
                  </li>
                </div>
              );
            })}
        </div>
      </div>
    </div>
  );
}
export default Favorites;
