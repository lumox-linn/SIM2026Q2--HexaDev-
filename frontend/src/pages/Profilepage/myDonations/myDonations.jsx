import { useEffect, useState } from "react";
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
  ConfigProvider,
} from "antd";
import { createStaticStyles } from "antd-style";
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";
import { apiMyDonations, apisearchHistory } from "../../../api";
import money from "../../../assets/money.svg";
import donate from "../../../assets/donate.svg";
import date from "../../../assets/date.svg";
import restart from "../../../assets/restart.svg";

function myDonations() {
  const location = useLocation();
  const userdata = localStorage.getItem("userData");
  const user = userdata ? JSON.parse(userdata) : null;

  const [data, setData] = useState([]);
  const [singleData, setsingleData] = useState({});
  const [allmoney, setallmoney] = useState(0);
  const [allcat, setallcat] = useState([]);
  const [selectv, setselectv] = useState(null);
  const [catid, setcatid] = useState(null);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [tableClass, settableClass] = useState(false);
  const [seeMore, setseeMore] = useState(false);

  // ── Helpers ───────────────────────────────────────────────
  const getStatusClass = (item) =>
    item.status === "suspended" ? "disabled" : "active";

  const mapItems = (list) =>
    list.map((item) => ({
      key:        item.donation_id,
      title:      item.title,
      category:   item.category_name,
      description: item.description,
      TargetMoney: item.target_amount,
      MoneyRaised: item.amount_raised,
      amount:     item.amount,
      Start:      item.start_date?.split(" ").slice(0, 4).join(" "),
      End:        item.end_date?.split(" ").slice(0, 4).join(" "),
      status:     item.status,
      donated_at: item.donated_at?.split(" ").slice(0, 4).join(" "),
    }));

  // ── percentage — raised / target ✅ fixed swap ─────────────
  const percentage = (item) => {
    const raised = parseFloat(item.MoneyRaised) || 0;
    const target = parseFloat(item.TargetMoney) || 0;
    if (target <= 0) return 0;
    return Math.round((raised / target) * 100);
  };

  // ── Styles ────────────────────────────────────────────────
  const styles = {
    root: { backgroundColor: "#e6f7ff" },
    icon: { color: "#52c41a" },
    content: { color: "#706d6d" },
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
    const hue = 200 - (200 * val) / 100;
    return {
      indicator: {
        backgroundImage: `linear-gradient(to right, hsla(${hue}, 85%, 65%, 1), hsla(${hue + 30}, 90%, 55%, 0.95))`,
        borderRadius: 8,
        transition: "all 0.3s ease",
      },
      rail: { backgroundColor: "rgba(0,0,0,0.1)", borderRadius: 8, height: "8px" },
    };
  };

  // ── Table row click ───────────────────────────────────────
  const see = (r) => {
    setseeMore(true);
    setsingleData(r);
    setData([r]);
    settableClass(true);
  };

  // ── Columns ───────────────────────────────────────────────
  const columns = [
    { title: "Title",       dataIndex: "title",       key: "title" },
    { title: "Category",    dataIndex: "category",    key: "category" },
    { title: "Target ($)",  dataIndex: "TargetMoney", key: "TargetMoney" },
    { title: "Start",       dataIndex: "Start",       key: "Start" },
    { title: "End",         dataIndex: "End",         key: "End" },
    {
      title: "Status",
      key: "status",
      dataIndex: "status",           // ✅ lowercase — matches data field
      render: (_, { status }) => (
        <Flex gap="small" align="center" wrap>
          <Tag color="green" key={status}>{status}</Tag>
        </Flex>
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="medium">
          <a style={{ color: "rgb(181, 117, 98)" }} onClick={() => see(record)}>
            See more
          </a>
        </Space>
      ),
    },
  ];

  // ── Refresh — load all donation history ───────────────────
  const refresh = () => {
    if (!user) return;
    apiMyDonations()
      .then((res) => {
        const activities = mapItems(res.history || []);
        setData(activities);

        // ✅ compute total from real data
        const total = activities.reduce(
          (sum, item) => sum + (parseFloat(item.amount) || 0), 0
        );
        setallmoney(total);

        // build category dropdown from history
        const uniqueCats = [...new Set(activities.map((i) => i.category).filter(Boolean))];
        setallcat(uniqueCats.map((name) => ({ value: name, label: name })));
      })
      .catch((err) => {
        console.log(err);
        message.error(err.response?.data?.error);
      });
  };

  useEffect(() => {
    refresh();
  }, []);

  // ── Search by category and/or date ───────────────────────
  const searchPro = () => {
    // build params from whatever is filled ✅
    const params = {};
    if (catid)     params.category_id = catid;
    if (startDate) params.start_date  = startDate;
    if (endDate)   params.end_date    = endDate;   // ✅ lowercase d

    if (Object.keys(params).length === 0) {
      setinpWarningVisi(true);
      return;
    }

    setinpWarningVisi(false);
    apisearchHistory(params)
      .then((res) => {
        const activities = mapItems(res.history || []);
        setData(activities);                        // ✅ actually updates table
      })
      .catch((err) => {
        console.log(err);
        message.error(err.response?.data?.error);
      });
  };

  const onSearch = (value) => console.log("search:", value);

  return (
    <div className="myDona">
      <li className="title">Donation History</li>

      <div className="mdContent">
        {/* ── Left panel ── */}
        <div className="leftc">
          <div className="personInfo">
            <div>
              <img src={user?.useravatar} alt="" />
            </div>
            <li>{user?.username || "Username"}</li>
            <li>{user?.useremail  || "Email"}</li>
            <li>{user?.userphone  || "Phone"}</li>
          </div>

          <div className="donations">
            <div className="totalD" style={{ backgroundColor: "rgba(240, 220, 132, 0.49)" }}>
              <li>
                <img src={donate} alt="" />
                Total Activities
              </li>
              <li style={{ paddingLeft: "20px" }}>
                &nbsp;&nbsp;
                <span style={{ fontSize: "25px" }}>{data.length}</span>  {/* ✅ dynamic */}
                &nbsp;
              </li>
              <li style={{ paddingLeft: "6px" }}>Activities you've supported</li>
            </div>

            <div className="money" style={{ backgroundColor: "rgba(197, 204, 130, 0.48)" }}>
              <li>
                <img src={money} alt="" />
                Total Contributions
              </li>
              <li style={{ fontSize: "25px", paddingLeft: "20px" }}>
                $ {allmoney}  {/* ✅ dynamic */}
              </li>
              <li>Total amount you've donated</li>
            </div>
          </div>
        </div>

        {/* ── Right panel ── */}
        <div className="allInfo">
          <div className="mdHead">
            <li>
              {/* Reset button */}
              <img
                src={restart}
                alt=""
                className="restart"
                onClick={() => {
                  setStartDate(null);
                  setEndDate(null);
                  setselectv(undefined);
                  setcatid(null);
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
                  value={startDate ? dayjs(startDate) : null}
                  onChange={(_, dateString) => setStartDate(dateString)}
                />
                -
                <DatePicker
                  style={{ width: "140px", height: "30px" }}
                  variant="borderless"
                  value={endDate ? dayjs(endDate) : null}
                  onChange={(_, dateString) => setEndDate(dateString)}
                />
              </ConfigProvider>

              {/* ✅ Category dropdown — catId stored directly in option */}
              <Select
                value={selectv}
                allowClear
                showSearch={{ optionFilterProp: "label", onSearch }}
                placeholder="Select a category"
                onChange={(value, option) => {
                  setselectv(value);
                  setcatid(option?.catId || null);  // ✅ no extra API call needed
                }}
                options={allcat.map((opt) => ({
                  value: opt.value,
                  label: opt.label,
                  catId: opt.catId,
                }))}
              />

              <button onClick={searchPro}>Search</button>

              {inpWarningVisi && (
                <span className="inpWarning">Please choose something to search!</span>
              )}
            </li>
          </div>

          {/* Table */}
          <div className={tableClass ? "onedata" : "tableS"}>
            <Table
              bordered="true"
              className="only-title-line"
              columns={columns}
              dataSource={data}
              rowKey="key"
              pagination={tableClass ? false : { pageSize: 6 }}
            />
          </div>

          {/* See more detail card */}
          {seeMore && (
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
                    {singleData.status === "active" ? "Active" : "Suspended"}
                  </div>
                  <p>
                    <Tag
                      classNames={classNames}
                      styles={styles}
                      icon={
                        singleData.status === "active"
                          ? <CheckCircleOutlined />
                          : <CloseCircleOutlined />
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
                  <p style={{ width: "100%", height: "20px", display: "flex", justifyContent: "space-between" }}>
                    <span style={{ color: "#6bacea" }}>Target: ${singleData.TargetMoney}</span>
                    <span style={{ color: "#b3bc4b" }}>Raised: ${singleData.MoneyRaised}</span>
                  </p>
                  <Flex vertical gap="large">
                    <Progress
                      classNames={progressClass}
                      styles={stylesFn}
                      percent={percentage(singleData)}
                    />
                  </Flex>
                  <hr />
                </li>

                <span style={{ marginBottom: "10px" }}>{singleData.description}</span>

                <li className="myD">
                  <span>
                    <img src={money} alt="" style={{ width: "30px", marginRight: "20px" }} />
                    My Contribution: &nbsp;${singleData.amount}
                  </span>
                  <span>
                    <img src={date} alt="" style={{ width: "30px", marginRight: "10px" }} />
                    Donation Date: &nbsp;{singleData.donated_at}
                  </span>
                </li>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default myDonations;