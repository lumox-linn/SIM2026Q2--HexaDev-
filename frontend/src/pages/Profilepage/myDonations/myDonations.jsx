import { useEffect, useState } from "react";
import cookie from "js-cookie";
import "./Myactivities.css";
import { message, Flex, Space, Table, Tag, Progress } from "antd";
import { createStaticStyles } from "antd-style";
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";
import { apiMyDonations } from "../../../api";
import money from "../../../assets/money.svg";
import donate from "../../../assets/donate.svg";
function myDonations() {
  const [userData, setuserData] = useState();
  const userdata = localStorage.getItem("userData");
  const [singleData, setsingleData] = useState({});
  const user = userdata ? JSON.parse(userdata) : null;
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [data, setData] = useState([]);
  const [tableClass, settableClass] = useState(false);

  const [inpValue, setinpvalue] = useState("");
  const [seeMore, setseeMore] = useState(false);
  const token = cookie.get("token");
  const getStatusClass = (item) => {
    if (item.status === "suspended") return "disabled";
    return "active";
  };
  const userDonate = {
    donate: "$1000",
    title: "Help the children learn",
    donateDate: "2026-03-02",
  };
  // const alldata = [
  //   {
  //     key: "1",
  //     title: "Help the children learn",
  //     category: "Education",
  //     TargetMoney: "$3000",
  //     MoneyRaised: "$1000",
  //     Start: "2026-01-01",
  //     End: "2026-03-06",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  // ];
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
  const searchProfile = (e) => {
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
  // table
  // const data = [
  //   {
  //     key: "1",
  //     title: "Help the children learn",
  //     category: "Education",
  //     TargetMoney: "$3000",
  //     MoneyRaised: "$1000",
  //     Start: "2026-01-01",
  //     End: "2026-03-06",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  //   {
  //     key: "2",
  //     title: "huhuhuhdushdu",
  //     category: "Animal",
  //     TargetMoney: "$4000",
  //     MoneyRaised: "$2000",
  //     Start: "2026-02-04",
  //     End: "2026-08-00",
  //     status: "Active",
  //   },
  // ];
  const searchPro = () => {
    // if the input has value
    if (inpValue !== "") {
      console.log(inpValue);
      // try {
      //   apiMyDonations(user.userid)
      //     .then((res) => {
      //       console.log(res);
      //     })
      //     .catch((err) => {
      //       message.error(err.response?.data?.error);
      //     });
      // } catch (error) {
      //   message.error(error.response?.data?.error);
      // }
    } else {
      // if the input value is empty
      setinpWarningVisi(true);
    }
  };

  const refresh = () => {
    console.log(user);
    console.log(token);
    try {
      apiMyDonations({ user_id: user.userid }, token)
        .then((res) => {
          // console.log("3333");
          // console.log(res);
          const activities = res.activities.map((item) => ({
            key: res.activity_id,

            title: res.title,
            category: res.category_name,
            TargetMoney: res.target_amount,
            MoneyRaised: res.amount_raised,
            Start: res.start_date,
            End: res.end_date,
            status: res.status,
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
            <li>username</li>
            <li>email</li>
            <li>phone</li>
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
                Total Activity
              </li>
              <li>
                &nbsp;&nbsp;
                <span style={{ fontSize: "25px" }}>3</span> &nbsp; Activities
              </li>
              <li>Total activities donated</li>
            </div>
            <div
              className="money"
              style={{
                backgroundColor: "rgba(197, 204, 130, 0.48)",
              }}
            >
              <li>
                <img src={money} alt="" />
                Total Amount
              </li>
              <li style={{ fontSize: "25px" }}>$ 3000</li>
              <li>Total amount of money donated</li>
            </div>
          </div>
        </div>

        <div className="allInfo">
          <div className="mdHead">
            <li>
              <input
                type="text"
                placeholder="Category name..."
                onChange={(e) => searchDonations(e)}
              />
              <button onClick={searchPro}>Search</button>
              {inpWarningVisi ? (
                <span className="inpWarning">
                  Please enter a category to search
                </span>
              ) : (
                ""
              )}
            </li>
          </div>

          <div className={tableClass ? "onedata" : "tableS"}>
            <Table
              bordered="true"
              className="only-title-line"
              columns={columns}
              dataSource={data}
              rowKey="user_id"
              pagination={
                tableClass
                  ? false
                  : {
                      pageSize: 8,
                    }
              }
            />
          </div>
          {/* key: "2",
      title: "huhuhuhdushdu",
      category: "Animal",
      TargetMoney: "$4000",
      MoneyRaised: "$2000",
      Start: "2026-02-04",
      End: "2026-08-00",
      status: "Active", */}
          {seeMore ? (
            <div className="seemore">
              <div className="cardView">
                <i
                  onClick={() => {
                    setData(alldata);
                    setseeMore(false);
                    settableClass(false);
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
                    {/* <span>{item.targetAmount}</span> */}
                    <Progress
                      classNames={progressClass}
                      styles={stylesFn}
                      percent={percentage(singleData)}
                    />
                  </Flex>
                  {/* <hr /> */}
                </li>

                {/* <span style={{ marginBottom: "45px" }}>{item.description}</span> */}
                <li className="myD">
                  <span>I donated: &nbsp;{userDonate.donate}</span>
                  <span>Date of donation: &nbsp; {userDonate.donateDate}</span>
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
