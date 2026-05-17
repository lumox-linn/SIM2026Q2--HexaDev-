import { useEffect, useState } from "react";
import cookie from "js-cookie";
import { useLocation } from "react-router-dom";
import "./Myactivities.css";
import dayjs from "dayjs";
import {
  message,
  Flex,
  Space,
  Table,
  Tag,
  Progress,
  Select,
  DatePicker,
  Form,
  ConfigProvider,
  TimePicker,
} from "antd";
const { RangePicker } = DatePicker;
import { createStaticStyles } from "antd-style";

import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";
import {
  apiMyDonations,
  apisearchHistory,
  apiGetDoneeActivities,
} from "../../../api";
import money from "../../../assets/money.svg";
import donate from "../../../assets/donate.svg";
import date from "../../../assets/date.svg";
import restart from "../../../assets/restart.svg";
function myDonations() {
  const location = useLocation();
  const [allcat, setallcat] = useState([]);
  const [userData, setuserData] = useState();
  const userdata = localStorage.getItem("userData");
  const [singleData, setsingleData] = useState({});
  const user = userdata ? JSON.parse(userdata) : null;
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [data, setData] = useState([]);
  const [tableClass, settableClass] = useState(false);
  const [selectv, setselectv] = useState(null);
  const [inpValue, setinpvalue] = useState("");
  const [seeMore, setseeMore] = useState(false);
  const [allmoney, setallmoney] = useState(0);
  const [catid, setcatid] = useState(0);
  const token = cookie.get("token");
  const userId = localStorage.getItem("userData");
  const getStatusClass = (item) => {
    if (item.status === "suspended") return "disabled";
    return "active";
  };
  const userDonate = {
    donate: "$1000",
    title: "Help the children learn",
    donateDate: "2026-03-02",
  };
  useEffect(() => {
    if (user) {
      setuserData(user);
    }
    // setData(alldata);

    refresh();
  }, []);
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
  const classNames = createStaticStyles(({ css }) => ({
    root: css`
      padding: 2px 6px;
      border-radius: 8px;
      margin-left: 10px;
    `,
  }));
  const progressClass = {
    root: "demo-progress-root",
    rail: "demo-progress-rail",
    track: "demo-progress-track",
  };
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
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
  const searchDonations = (e) => {
    setinpvalue(e.target.value);
    // when input value changed,set warning to invisible
    if (e.target.value !== "") {
      setinpWarningVisi(false);
    } else {
      // if the input value is empty, refresh data
      refresh();
    }
  };

  const percentage = (item) => {
    const raised = parseFloat(item.TargetMoney) || 0;
    const target = parseFloat(item.MoneyRaised) || 0;
    if (target <= 0) return 0;
    const res = Math.round((raised / target) * 100);

    return res;
  };

  // single row action
  const see = (r) => {
    setseeMore(true);
    setsingleData(r);
    setData([r]);
    settableClass(true);
  };
  // table
  const columns = [
    {
      title: "Title",
      dataIndex: "title",
      key: "title",

      // render: (text) => <a >{text}</a>,
    },
    {
      title: "category",
      dataIndex: "category",
      key: "category",
    },
    {
      title: "TargetMoney",
      dataIndex: "TargetMoney",
      key: "TargetMoney",
    },
    {
      title: "Start",
      dataIndex: "Start",
      key: "Start",
    },
    {
      title: "End",
      dataIndex: "End",
      key: "End",
    },
    {
      title: "Status",
      key: "Status",
      dataIndex: "Status",
      render: (_, { status }) => (
        <Flex gap="small" align="center" wrap>
          <Tag color="green" key={status}>
            {status}
          </Tag>
        </Flex>
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="medium">
          <a
            style={{ color: " rgb(181, 117, 98)" }}
            onClick={() => see(record)}
          >
            See more{record.name}
          </a>
          <a
            style={{ color: " rgb(120, 184, 83)" }}
            onClick={() => see(record)}
          >
            Donate again
          </a>
        </Space>
      ),
    },
  ];
  const searchPro = () => {
    console.log(startDate, endDate, selectv);
    if ((startDate && endDate) || catid) {
      try {
        apisearchHistory(
          selectv
            ? { category_id: catid }
            : { start_date: startDate, end_Date: endDate },
        )
          .then((res) => {
            const backendList = res.history;
            console.log(res);
            const activities = backendList.map((item) => ({
              key: item.donation_id,
              description: item.description,
              amount: item.amount,
              donated_at: item.donated_at?.split(" ").slice(0, 4).join(" "),
              title: item.title,
              category: item.category_name,
              TargetMoney: item.target_amount,
              MoneyRaised: item.amount_raised,
              Start: item.start_date?.split(" ").slice(0, 4).join(" "),
              End: item.end_date?.split(" ").slice(0, 4).join(" "),
              status: item.status,
            }));
            setData(activities);
          })
          .catch((err) => {
            console.log(err);
            message.error(err.response?.data?.error);
          });
      } catch (error) {
        message.error(error.response?.data?.error);
      }
    } else {
      // if the input value is empty
      setinpWarningVisi(true);
    }
  };

  const refresh = () => {
    console.log(user);
    console.log(inpValue);
    if (!user) return;
    try {
      const apiParams = {
        user_id: user.userid,
      };

      apiMyDonations()
        .then((res) => {
          const backendList = res.history;
          console.log(res);
          const activities = backendList.map((item) => ({
            key: item.donation_id,
            description: item.description,
            amount: item.amount,
            donated_at: item.donated_at?.split(" ").slice(0, 4).join(" "),
            title: item.title,
            category: item.category_name,
            TargetMoney: item.target_amount,
            MoneyRaised: item.amount_raised,
            Start: item.start_date?.split(" ").slice(0, 4).join(" "),
            End: item.end_date?.split(" ").slice(0, 4).join(" "),
            status: item.status,
          }));
          setData(activities);

          const totalAmount = activities.reduce((prev, curr) => {
            const currentAmount = parseFloat(curr.amount) || 0;
            return prev + currentAmount;
          }, 0);

          setallmoney(totalAmount);
          const uniqueCategoryNamess = [
            ...new Set(activities.map((item) => item.category)),
          ];

          const selectOptions = uniqueCategoryNamess.map((name) => ({
            value: name,
            label: name,
          }));
          setallcat(selectOptions);
        })
        .catch((err) => {
          console.log(err);
          message.error(err.response?.data?.error);
        });
    } catch (error) {
      message.error(error.response?.data?.error);
    }
  };

  const onChange = (value) => {
    console.log(value);
    if (value) {
      // const newdata = activityData.find((item) => item.category == value);
      // console.log(newdata);
      // setactivityData([newdata]);
    } else {
      // refresh();
    }
  };
  const onSearch = (value) => {
    console.log("search:", value);
  };
  return (
    <div className="myDona">
      <li className="title">Donation History</li>

      <div className="mdContent">
        <div className="leftc">
          <div className="personInfo">
            <div>
              <img src={user.useravatar} alt="" />
            </div>
            <li>{user?.username || "Username"}</li>
            <li>{user?.useremail || "Email"}</li>
            <li>{user?.userphone || "Phone"}</li>
          </div>
          <div className="donations">
            <div
              className="totalD"
              style={{
                backgroundColor: "rgba(240, 220, 132, 0.49)",
              }}
            >
              <li>
                <img src={donate} alt="" />
                Total Activities
              </li>
              <li style={{ paddingLeft: "20px" }}>
                &nbsp;&nbsp;
                <span style={{ fontSize: "25px" }}>{data.length}</span> &nbsp;
              </li>
              <li style={{ paddingLeft: "6px" }}>
                Activities you've supported
              </li>
            </div>
            <div
              className="money"
              style={{
                backgroundColor: "rgba(197, 204, 130, 0.48)",
              }}
            >
              <li>
                <img src={money} alt="" />
                Total Contributions
              </li>
              <li style={{ fontSize: "25px", paddingLeft: "20px" }}>
                $ {allmoney}
              </li>
              <li>Total amount you've donated</li>
            </div>
          </div>
        </div>

        <div className="allInfo">
          <div className="mdHead">
            <li>
              <img
                src={restart}
                alt=""
                className="restart"
                onClick={() => {
                  setStartDate(null);
                  setEndDate(null);
                  setselectv(undefined);
                  setinpWarningVisi(false);
                  refresh();
                }}
              />
              Date:
              <ConfigProvider
                theme={{
                  components: {
                    DatePicker: {
                      colorPrimary: "#78b853",
                      colorLink: "#78b853",
                      activeBorderColor: "#78b853",
                      hoverBorderColor: "#62b580",
                      borderRadius: 4,
                      cellHoverBg: "rgba(120, 184, 83, 0.1)",
                    },
                  },
                }}
              >
                <DatePicker
                  style={{ width: "140px", height: "30px" }}
                  variant="borderless"
                  onChange={(date, dateString) => {
                    setStartDate(dateString);
                  }}
                  value={startDate ? dayjs(startDate) : null}
                />
                -
                <DatePicker
                  style={{ width: "140px", height: "30px" }}
                  variant="borderless"
                  onChange={(date, dateString) => {
                    setEndDate(dateString);
                  }}
                  value={endDate ? dayjs(endDate) : null}
                />
              </ConfigProvider>
              <Select
                value={selectv}
                allowClear
                showSearch={{ optionFilterProp: "label", onSearch }}
                placeholder="Select a category"
                onChange={(value) => {
                  // const uniqueCategoryNamess = [
                  //   ...new Set(data.map((item) => item.category)),
                  // ];
                  setselectv(value);
                  apiGetDoneeActivities({ user_id: userId })
                    .then((res) => {
                      console.log(res);

                      if (value !== null) {
                        const selectOptions = res.activities.find((item) => {
                          return item.category_name == value;
                        });
                        console.log(selectOptions);

                        setcatid(selectOptions.category_id);
                      }
                    })
                    .catch((err) => {
                      console.log(err);
                      message.error(err.response?.data?.error);
                    });
                }}
                options={allcat}
              />
              <button onClick={searchPro}>Search</button>
              {inpWarningVisi ? (
                <span className="inpWarning">
                  Please choose something to search!
                </span>
              ) : (
                ""
              )}
            </li>
          </div>

          {/* <div className={tableClass ? "onedata" : "tableS"}>
            {
              data.map((item)=>{
                return 
              })
            } */}

          <div className={tableClass ? "onedata" : "tableS"}>
            <Table
              bordered="true"
              className="only-title-line"
              columns={columns}
              dataSource={data}
              rowKey="key"
              pagination={
                tableClass
                  ? false
                  : {
                      pageSize: 6,
                    }
              }
            />
          </div>

          {seeMore ? (
            <div className="seemore">
              <div className="cardView">
                <i
                  onClick={() => {
                    setseeMore(false);
                    settableClass(false);
                    refresh();
                  }}
                  className="closeView"
                >
                  X
                </i>

                <li className="first">
                  <span className="name">{singleData.title}</span>

                  <div className={getStatusClass(singleData)}>
                    {singleData.status === "Active" ? "Active" : "Suspended"}
                  </div>

                  <p>
                    <Tag
                      classNames={classNames}
                      styles={styles}
                      icon={
                        singleData.status === "Active" ? (
                          <CheckCircleOutlined />
                        ) : (
                          <CloseCircleOutlined />
                        )
                      }
                    >
                      {singleData.category}
                    </Tag>
                  </p>
                </li>

                <li className="date">
                  <p>
                    <span>Start date: {singleData.Start}</span>
                    <span style={{ marginLeft: "30px", color: "#eb2f2f" }}>
                      End date: {singleData.End}
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
                      Target: ${singleData.TargetMoney}
                    </span>
                    <span style={{ color: "#b3bc4b" }}>
                      Raised: ${singleData.MoneyRaised}
                    </span>
                  </p>
                  <Flex vertical gap="large">
                    <span>{singleData.targetAmount}</span>
                    <Progress
                      classNames={progressClass}
                      styles={stylesFn}
                      percent={percentage(singleData)}
                    />
                  </Flex>
                  <hr />
                </li>

                <span style={{ marginBottom: "10px" }}>
                  {singleData.description}
                </span>
                <li className="myD">
                  <span>
                    <img
                      src={money}
                      alt=""
                      style={{
                        width: "30px",
                        marginRight: "20px",
                      }}
                    />
                    My Contribution: &nbsp;${singleData.amount}
                  </span>
                  <span>
                    <img
                      src={date}
                      alt=""
                      style={{ width: "30px", marginRight: "10px" }}
                    />
                    Donation Date: &nbsp; {singleData.donated_at}
                  </span>
                </li>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}
export default myDonations;
