import "../Activities/activities.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  DownOutlined,
  LogoutOutlined,
  SettingOutlined,
} from "@ant-design/icons";
import { createStyles } from "antd-style";
import dayjs from "dayjs";
import {
  apiGetDoneeActivities,
  apiDeleteActivities,
  apiSaveFavourite,
  apiViewActivity,
  apisearchActivities,
} from "../../api";
import { createStaticStyles } from "antd-style";
import heart from "../../assets/heart.svg";

import {
  Button,
  Dropdown,
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
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";
function ActivityStatus() {
  const location = useLocation();
  const [activityData, setactivityData] = useState([]);
  const userdata = location.state?.userdata || {};
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const userId = localStorage.getItem("userData")
    ? JSON.parse(localStorage.getItem("userData")).userid
    : null;
  const [inpValue, setinpvalue] = useState("");
  const [allcat, setallcat] = useState([]);
  const [creaVisi, setcreaVisi] = useState(false);
  const [buttype, setbuttype] = useState("");
  const { TextArea } = Input;
  const [form] = Form.useForm();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedActivities, setselectedActivities] = useState(null);
  const [editValue, setEditValue] = useState(null);
  const [viewActivity, setViewActivity] = useState({
    viewstatus: false,
    actId: null,
  });

  // const [cat, setcat] = useState(null);
  const [allcategories, setallCategories] = useState([
    { category: "Animal", catId: 2 },
    { category: "Education", catId: 3 },
    { category: "Environment", catId: 5 },
    { category: "Health", catId: 4 },
    { category: "School", catId: 1 },
  ]);
  const [targetNumber, settargetNumber] = useState(false);
  const percentage = (item) => {
    const raised = parseFloat(item.amount_raised) || 0;
    const target = parseFloat(item.target_amount) || 0;
    if (target <= 0) return 0;
    const res = Math.round((raised / target) * 100);

    return res;
  };
  const progressClass = {
    root: "demo-progress-root",
    rail: "demo-progress-rail",
    track: "demo-progress-track",
  };
  const styles = {
    root: {
      backgroundColor: "#e6f7ff",
      borderRadius: "10px",
    },
    icon: {
      color: "#52c41a",
    },
    content: {
      color: "#706d6d",
    },
  };

  const classNames = createStaticStyles(({ css }) => ({
    root: css`
      padding: 2px 6px;
      border-radius: 8px;
      margin-left: 10px;
    `,
  }));

  const showModal = (profile) => {
    setselectedActivities(profile);
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
    if (!selectedActivities) return;
    console.log(selectedActivities);
    // try {
    //   apiDeleteActivities(selectedActivities.activity_id)
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
  const searchAccount = (e) => {
    setinpvalue(e.target.value);
    // when input value changed,set warning to invisible
    if (e.target.value !== "") {
      setinpWarningVisi(false);
    } else {
      // if the input value is empty, refresh data
      refresh();
    }
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
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const refresh = () => {
    console.log(userId);
    try {
      apiGetDoneeActivities({ user_id: userId })
        .then((res) => {
          console.log(res);
          if (res.activities) {
            const activities = res.activities.map((item) => ({
              activity_id: item.activity_id,
              title: item.title,
              description: item.description,
              amount_raised: item.amount_raised,
              category: item.category_name,
              status: item.status,
              created_at: item.created_at.split(" ").slice(0, 4).join(" "),
              creator: item.creator,
              target_amount: item.target_amount,
              category_name: item.category_name,
              start_date: item.start_date?.split(" ").slice(0, 4).join(" "),
              // start_date: item.start_date.split(" ").slice(0, 4).join(" "),
              end_date: item.end_date?.split(" ").slice(0, 4).join(" "),
              // end_date: item.end_date.split(" ").slice(0, 4).join(" "),
            }));
            setactivityData(activities);
            const uniqueCategoryNames = [
              ...new Set(activities.map((item) => item.category_name)),
            ];

            const selectOptions = uniqueCategoryNames.map((name) => ({
              value: name,
              label: name,
            }));

            setallcat(selectOptions);
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
  const viewAct = (item) => {
    setViewActivity({
      viewstatus: true,
      actId: item.activity_id,
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const searchActivities = (e) => {
    setinpvalue(e.target.value);
    // when input value changed,set warning to invisible
    if (e.target.value !== "") {
      setinpWarningVisi(false);
    } else {
      // if the input value is empty, refresh data
      refresh();
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const searchPro = () => {
    // if the input has value
    if (inpValue !== "") {
      console.log(inpValue);
      try {
        apisearchActivities({ query: inpValue })
          .then((res) => {
            console.log(res);
            if (res.activities) {
              const activities = res.activities.map((item) => ({
                activity_id: item.activity_id,
                title: item.title,
                description: item.description,
                amount_raised: item.amount_raised,
                category: item.category_name,
                status: item.status,
                created_at: item.created_at.split(" ").slice(0, 4).join(" "),
                creator: item.creator,
                target_amount: item.target_amount,
                category_name: item.category_name,
                start_date: item.start_date?.split(" ").slice(0, 4).join(" "),
                // start_date: item.start_date.split(" ").slice(0, 4).join(" "),
                end_date: item.end_date?.split(" ").slice(0, 4).join(" "),
                // end_date: item.end_date.split(" ").slice(0, 4).join(" "),
              }));
              setactivityData(activities);
            }
          })
          .catch((err) => {
            // console.log(err);
            message.error(err.response?.data?.error);
          });
      } catch (error) {
        // console.log(error);
        message.error(error.response?.data?.error);
      }
    } else {
      // if the input value is empty
      setinpWarningVisi(true);
    }
  };

  const getStatusClass = (item) => {
    if (item.status === "suspended") return "disabled";
    return "active";
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  const onChange = (value) => {
    console.log(value);
    if (value) {
      const newdata = activityData.find((item) => item.category == value);
      console.log(newdata);
      setactivityData([newdata]);
    } else {
      refresh();
    }
  };
  const onSearch = (value) => {
    console.log("search:", value);
  };
  const saveAct = (item) => {
    try {
      apiSaveFavourite(item.activity_id)
        .then((res) => {
          if (res.status == "success") {
            message.success(res.message);
          }
        })
        .catch((err) => {
          // console.log(err);
          message.error(err.response?.data?.error);
        });
    } catch (error) {
      message.error(error.response?.data?.error);
    }
  };

  return (
    <div className="mc">
      <div className="pmhead">
        <span className="title">Browse fundraising activities</span>
        <li>
          <input
            type="text"
            placeholder="Search Activities..."
            onChange={(e) => searchActivities(e)}
          />
          <button onClick={searchPro} className="searchb">
            Search
          </button>
          {inpWarningVisi ? (
            <span className="inpWarning">
              Please enter a activity to search
            </span>
          ) : (
            ""
          )}
          <Select
            allowClear
            showSearch={{ optionFilterProp: "label", onSearch }}
            placeholder="Select a category"
            onChange={onChange}
            options={allcat}
          />
        </li>
      </div>

      <div className="activityContent">
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
                  item.activity_id === viewActivity.actId ? "cardView" : "card"
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
                      {item.category}
                    </Tag>
                  </p>

                  <button className="save" onClick={() => saveAct(item)}>
                    Save
                  </button>
                </li>
                {item.activity_id === viewActivity.actId ? (
                  <li className="date">
                    <p>
                      <span>
                        Start date:{" "}
                        {item.start_date == null ? "null" : item.start_date}
                      </span>
                      <span style={{ marginLeft: "30px", color: "#eb2f2f" }}>
                        End date:{" "}
                        {item.end_date == null ? "null" : item.end_date}
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

                <span style={{ marginBottom: "45px" }}>{item.description}</span>

                <li
                  className="butStyle"
                  style={{
                    position: "absolute",
                    bottom: "13px",
                    zIndex: 10,
                    left: "19px",
                  }}
                >
                  <button className="donate">
                    <img src={heart} alt="" className="heart" />
                    Donate
                  </button>

                  {viewActivity.actId == item.activity_id ? null : (
                    <button
                      onClick={() => {
                        viewAct(item);
                        if (creaVisi) {
                          setcreaVisi(!creaVisi);
                        }

                        try {
                          apiViewActivity(item.activity_id)
                            .then((res) => {
                              console.log(res);
                            })
                            .catch((err) => {
                              message.error(err.response?.data?.error);
                            });
                        } catch (error) {
                          message.error(error.response?.data?.error);
                        }
                      }}
                    >
                      View
                    </button>
                  )}

                  <Modal
                    title="Suspension Confirmation"
                    open={isModalOpen}
                    onOk={handleOk}
                    onCancel={handleCancel}
                    okText="Delete"
                    okType="danger"
                    className="modall"
                  >
                    <p>
                      Are you sure you want to delete the Activities
                      <b> {selectedActivities?.title}?</b>
                    </p>
                  </Modal>
                </li>
              </div>
            );
          })}
      </div>
    </div>
  );
}
export default ActivityStatus;
