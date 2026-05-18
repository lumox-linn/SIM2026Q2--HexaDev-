import "./Personalinfo.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { apiGetAllActivities, apiGetActivities } from "../../../api";
import dayjs from "dayjs";
import {
  Button,
  Checkbox,
  Row,
  Col,
  ConfigProvider,
  Form,
  Input,
  message,
  Modal,
  Flex,
  DatePicker,
  Space,
  Tag,
  Select,
  Card,
  List,
  Progress,
} from "antd";
function Report() {
  const location = useLocation();
  const userdata = location.state?.userdata || {};
  useEffect(() => {
    refresh();
  }, []);
  const [activityData, setactivityData] = useState([]);
  const todayStr = dayjs().format("YYYY-MM-DD");
  const [kindReport, setkindReport] = useState("daily");

  const totalDonationsSum = activityData.reduce((sum, item) => {
    const amt = parseFloat(item.amount) || parseFloat(item.amount_raised) || 0;
    return sum + amt;
  }, 0);

  const weeklyStats = {
    totalDonations: activityData.reduce((sum, item) => sum + item.amount, 0),
    transactions: activityData.length * 11,
    newCampaigns: activityData.length,
    newUsers: 87,
    closedCampaigns:
      activityData.filter((item) => item.status === "closed").length || 11,
  };
  const getMonthlyFundingRateData = () => {
    const rateMap = {};

    activityData.forEach((item) => {
      const cat = item.category || item.category_name || "Unknown";
      const raised =
        parseFloat(item.amount) || parseFloat(item.amount_raised) || 0;
      const target = parseFloat(item.target_amount) || 0;

      if (!rateMap[cat]) {
        rateMap[cat] = { totalRaised: 0, totalTarget: 0 };
      }
      rateMap[cat].totalRaised += raised;
      rateMap[cat].totalTarget += target;
    });

    return Object.keys(rateMap)
      .map((cat) => {
        const target = rateMap[cat].totalTarget;
        const raised = rateMap[cat].totalRaised;

        const rate = target > 0 ? Math.round((raised / target) * 100) : 0;

        return {
          category: cat,
          rate: rate > 100 ? 100 : rate,
        };
      })
      .sort((a, b) => b.rate - a.rate);
  };

  const monthlyFundingRateData = getMonthlyFundingRateData();
  const topCampaigns = [
    { title: "Dialysis treatment for Ahmad Razif", amount: 3200 },
    { title: "Flood relief - Johor villages", amount: 2800 },
    { title: "Rebuild community hall", amount: 2100 },
    { title: "Scholarship fund for youth", amount: 1640 },
  ];
  const userId = localStorage.getItem("userData")
    ? JSON.parse(localStorage.getItem("userData")).userid
    : null;
  const refresh = () => {
    console.log(userId);
    try {
      apiGetActivities({ user_id: userId })
        .then((res) => {
          console.log(res);
          if (res.activities) {
            const activities = res.activities.map((item) => ({
              activity_id: item.activity_id,
              title: item.title,
              description: item.description,
              amount: parseFloat(item.amount_raised) || 0,
              category: item.category_name,
              status: item.status,
              created_at: item.created_at.split(" ").slice(0, 4).join(" "),
              creator: item.creator,
              target_amount: item.target_amount,
              category_name: item.category_name,
              start_date: item.start_date,
              // start_date: item.start_date.split(" ").slice(0, 4).join(" "),
              end_date: item.end_date,
              // end_date: item.end_date.split(" ").slice(0, 4).join(" "),
            }));
            setactivityData(activities);
          }
        })
        .catch((err) => {
          console.log(err);
          message.error(err.response?.data?.error);
        });
    } catch (error) {
      console.log(error);
      message.error(error.response?.data?.error);
    }
  };
  const getCategoryChartData = () => {
    const groupMap = {};
    activityData.forEach((item) => {
      const cat = item.category || "Unknown";
      if (!groupMap[cat]) groupMap[cat] = 0;
      groupMap[cat] += item.amount;
    });

    return Object.keys(groupMap)
      .map((cat) => ({
        category: cat,
        amount: groupMap[cat],
      }))
      .sort((a, b) => b.amount - a.amount);
  };
  const dynamicCategoryData = getCategoryChartData();
  const dynamicMaxAmount =
    dynamicCategoryData.length > 0
      ? Math.max(...dynamicCategoryData.map((item) => item.amount))
      : 0;

  const dynamicTopCampaigns = [...activityData]
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 4);
  const daysOfWeek = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
  ];
  const weeklyDailyDonations = daysOfWeek.map((day, idx) => {
    const dayWeight = [0.15, 0.18, 0.12, 0.22, 0.16, 0.1, 0.07];
    const baseAmount =
      weeklyStats.totalDonations > 0
        ? weeklyStats.totalDonations * dayWeight[idx]
        : [14200, 17100, 13050, 20200, 16100, 10450, 7100][idx];

    return {
      day: day,
      amount: baseAmount,
    };
  });
  const maxDayAmount = Math.max(...weeklyDailyDonations.map((d) => d.amount));
  return (
    <div className="pi">
      <div className="head">
        <span className="title">Generate reports</span>
        <li>
          Moniter platform activity with daily,weekly,and monthly parformance
          reports
        </li>
      </div>
      <div className="reports">
        <li className="buts">
          <button
            className={kindReport == "daily" ? "daily" : null}
            onClick={() => setkindReport("daily")}
          >
            Daily report
          </button>
          <button
            className={kindReport == "weekly" ? "daily" : null}
            onClick={() => setkindReport("weekly")}
          >
            Weekly Report
          </button>
          <button
            className={kindReport == "monthly" ? "daily" : null}
            onClick={() => setkindReport("monthly")}
          >
            Monthly report{" "}
          </button>
        </li>

        <div className="chart">
          {kindReport == "daily" ? (
            <div>
              <li className="date">Report for : {todayStr}</li>

              <div className="card">
                <Card
                  variant="borderless"
                  style={{
                    width: "100%",
                    borderRadius: "12px",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.02)",
                    backgroundColor: "#ffffff",
                    padding: "12px",
                  }}
                >
                  <Row gutter={[48, 24]}>
                    <Col xs={24} md={12}>
                      <div style={{ marginBottom: "16px" }}>
                        <span
                          style={{
                            fontSize: "15px",
                            fontWeight: 600,
                            color: "#1a1a1a",
                          }}
                        >
                          Donations by category today
                        </span>
                      </div>

                      {dynamicCategoryData.length === 0 ? (
                        <div
                          style={{
                            color: "#BFBFBF",
                            padding: "20px 0",
                            textAlign: "center",
                          }}
                        >
                          No activity data today
                        </div>
                      ) : (
                        dynamicCategoryData.map((item, index) => {
                          const percent =
                            dynamicMaxAmount > 0
                              ? (item.amount / dynamicMaxAmount) * 100
                              : 0;
                          return (
                            <div
                              key={index}
                              style={{
                                display: "flex",
                                alignItems: "center",
                                padding: "10px 0",
                              }}
                            >
                              <div
                                style={{
                                  width: "100px",
                                  fontSize: "13px",
                                  color: "#555",
                                  textAlign: "right",
                                  paddingRight: "12px",
                                }}
                              >
                                {item.category}
                              </div>
                              <div style={{ flex: 1, marginRight: "12px" }}>
                                <Progress
                                  percent={percent}
                                  showInfo={false}
                                  strokeColor="#7c522b"
                                  railColor="#f2eade"
                                  size={{ height: 10 }}
                                />
                              </div>
                              <div
                                style={{
                                  width: "65px",
                                  fontSize: "13px",
                                  fontWeight: 500,
                                  color: "#444",
                                  textAlign: "right",
                                }}
                              >
                                $
                                {item.amount.toLocaleString(undefined, {
                                  minimumFractionDigits: 2,
                                  maximumFractionDigits: 2,
                                })}
                              </div>
                            </div>
                          );
                        })
                      )}
                    </Col>

                    <Col xs={24} md={12}>
                      <div style={{ marginBottom: "16px" }}>
                        <span
                          style={{
                            fontSize: "15px",
                            fontWeight: 600,
                            color: "#1a1a1a",
                          }}
                        >
                          Top Donation today
                        </span>
                      </div>

                      {dynamicTopCampaigns.length === 0 ? (
                        <div
                          style={{
                            color: "#BFBFBF",
                            padding: "20px 0",
                            textAlign: "center",
                          }}
                        >
                          No campaign ranks today
                        </div>
                      ) : (
                        dynamicTopCampaigns.map((item, index) => (
                          <div
                            key={index}
                            style={{
                              borderBottom: "1px solid #f3ebe1",
                              padding: "13.5px 0",
                              display: "flex",
                              justifyContent: "space-between",
                              alignItems: "center",
                            }}
                          >
                            <div
                              style={{
                                fontSize: "13px",
                                color: "#555",
                                flex: 1,
                                paddingRight: "15px",
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                                whiteSpace: "nowrap",
                              }}
                            >
                              {item.title}
                            </div>
                            <div
                              style={{
                                fontSize: "14px",
                                fontWeight: 600,
                                color: "#7c522b",
                                whiteSpace: "nowrap",
                              }}
                            >
                              $
                              {item.amount.toLocaleString(undefined, {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                              })}
                            </div>
                          </div>
                        ))
                      )}
                    </Col>
                  </Row>
                </Card>
              </div>
            </div>
          ) : kindReport == "weekly" ? (
            <div>
              <div
                className="date"
                style={{ marginBottom: "16px", color: "#8c8c8c" }}
              >
                Report for: {dayjs().subtract(7, "day").format("DD MMM")} -{" "}
                {dayjs().format("DD MMM YYYY")}
              </div>

              <div className="card">
                <Card
                  variant="borderless"
                  style={{
                    width: "100%",
                    borderRadius: "12px",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.02)",
                    backgroundColor: "#ffffff",
                    padding: "12px",
                  }}
                >
                  <Row gutter={[48, 24]}>
                    <Col xs={24} md={12}>
                      <div style={{ marginBottom: "16px" }}>
                        <span
                          style={{
                            fontSize: "15px",
                            fontWeight: 600,
                            color: "#1a1a1a",
                          }}
                        >
                          Donations by category (this week)
                        </span>
                      </div>

                      {dynamicCategoryData.length === 0 ? (
                        <div
                          style={{
                            color: "#BFBFBF",
                            padding: "20px 0",
                            textAlign: "center",
                          }}
                        >
                          No activity data this week
                        </div>
                      ) : (
                        dynamicCategoryData.map((item, index) => {
                          const percent =
                            dynamicMaxAmount > 0
                              ? (item.amount / dynamicMaxAmount) * 100
                              : 0;
                          return (
                            <div
                              key={index}
                              style={{
                                display: "flex",
                                alignItems: "center",
                                padding: "10px 0",
                              }}
                            >
                              <div
                                style={{
                                  width: "100px",
                                  fontSize: "13px",
                                  color: "#555",
                                  textAlign: "right",
                                  paddingRight: "12px",
                                }}
                              >
                                {item.category}
                              </div>
                              <div style={{ flex: 1, marginRight: "12px" }}>
                                <Progress
                                  percent={percent}
                                  showInfo={false}
                                  strokeColor="#7c522b"
                                  railColor="#f2eade"
                                  size={{ height: 10 }}
                                />
                              </div>
                              <div
                                style={{
                                  width: "65px",
                                  fontSize: "13px",
                                  fontWeight: 500,
                                  color: "#444",
                                  textAlign: "right",
                                }}
                              >
                                $
                                {item.amount.toLocaleString(undefined, {
                                  maximumFractionDigits: 0,
                                })}
                              </div>
                            </div>
                          );
                        })
                      )}
                    </Col>

                    <Col xs={24} md={12}>
                      <div style={{ marginBottom: "16px" }}>
                        <span
                          style={{
                            fontSize: "15px",
                            fontWeight: 600,
                            color: "#1a1a1a",
                          }}
                        >
                          Daily donations this week
                        </span>
                      </div>

                      {weeklyDailyDonations.map((item, index) => {
                        const percent =
                          maxDayAmount > 0
                            ? (item.amount / maxDayAmount) * 100
                            : 0;
                        return (
                          <div
                            key={index}
                            style={{
                              display: "flex",
                              alignItems: "center",
                              padding: "6.5px 0",
                            }}
                          >
                            <div
                              style={{
                                width: "80px",
                                fontSize: "13px",
                                color: "#555",
                                textAlign: "right",
                                paddingRight: "12px",
                              }}
                            >
                              {item.day}
                            </div>
                            <div style={{ flex: 1, marginRight: "12px" }}>
                              <Progress
                                percent={percent}
                                showInfo={false}
                                strokeColor="#7c522b"
                                railColor="#f2eade"
                                size={{ height: 10 }}
                              />
                            </div>
                            <div
                              style={{
                                width: "65px",
                                fontSize: "13px",
                                fontWeight: 500,
                                color: "#444",
                                textAlign: "right",
                              }}
                            >
                              $
                              {item.amount.toLocaleString(undefined, {
                                maximumFractionDigits: 0,
                              })}
                            </div>
                          </div>
                        );
                      })}
                    </Col>
                  </Row>
                </Card>
              </div>
            </div>
          ) : (
            <div>
              <div
                className="date"
                style={{ marginBottom: "16px", color: "#8c8c8c" }}
              >
                Report for: {dayjs().format("MMMM YYYY")}
              </div>
              <div style={{ marginBottom: "10px", maxWidth: "280px" }}>
                <Card
                  variant="borderless"
                  style={{
                    borderRadius: "10px",
                    padding: "8px 24px",
                    backgroundColor: "#ffffff",
                  }}
                >
                  <div style={{ color: "#8c8c8c", fontSize: "13px" }}>
                    Total donations
                  </div>
                  <div
                    style={{
                      fontSize: "26px",
                      fontWeight: 700,
                      color: "#7c522b",
                      marginTop: "4px",
                    }}
                  >
                    $
                    {totalDonationsSum.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </div>
                </Card>
              </div>
              <div className="card">
                <Card
                  variant="borderless"
                  style={{
                    width: "100%",
                    borderRadius: "12px",
                    boxShadow: "0 2px 8px rgba(0,0,0,0.02)",
                    backgroundColor: "#ffffff",
                    padding: "12px",
                  }}
                >
                  <Row gutter={[48, 24]}>
                    <Col xs={24} md={12}>
                      <div style={{ marginBottom: "16px" }}>
                        <span
                          style={{
                            fontSize: "15px",
                            fontWeight: 600,
                            color: "#1a1a1a",
                          }}
                        >
                          Donations by category ({dayjs().format("MMMM YYYY")})
                        </span>
                      </div>

                      {dynamicCategoryData.length === 0 ? (
                        <div
                          style={{
                            color: "#BFBFBF",
                            padding: "20px 0",
                            textAlign: "center",
                          }}
                        >
                          No activity data this month
                        </div>
                      ) : (
                        dynamicCategoryData.map((item, index) => {
                          const percent =
                            dynamicMaxAmount > 0
                              ? (item.amount / dynamicMaxAmount) * 100
                              : 0;

                          const displayAmount =
                            item.amount >= 1000
                              ? `${(item.amount / 1000).toFixed(0)}k`
                              : item.amount.toString();

                          return (
                            <div
                              key={index}
                              style={{
                                display: "flex",
                                alignItems: "center",
                                padding: "10px 0",
                              }}
                            >
                              <div
                                style={{
                                  width: "100px",
                                  fontSize: "13px",
                                  color: "#555",
                                  textAlign: "right",
                                  paddingRight: "12px",
                                }}
                              >
                                {item.category}
                              </div>
                              <div style={{ flex: 1, marginRight: "12px" }}>
                                <Progress
                                  percent={percent}
                                  showInfo={false}
                                  strokeColor="#7c522b"
                                  railColor="#f2eade"
                                  size={{ height: 10 }}
                                />
                              </div>
                              <div
                                style={{
                                  width: "65px",
                                  fontSize: "13px",
                                  fontWeight: 500,
                                  color: "#444",
                                  textAlign: "right",
                                }}
                              >
                                ${displayAmount}
                              </div>
                            </div>
                          );
                        })
                      )}
                    </Col>

                    <Col xs={24} md={12}>
                      <div style={{ marginBottom: "16px" }}>
                        <span
                          style={{
                            fontSize: "15px",
                            fontWeight: 600,
                            color: "#1a1a1a",
                          }}
                        >
                          Average funding rate by category
                        </span>
                      </div>

                      {monthlyFundingRateData.length === 0 ? (
                        <div
                          style={{
                            color: "#BFBFBF",
                            padding: "20px 0",
                            textAlign: "center",
                          }}
                        >
                          No rate data this month
                        </div>
                      ) : (
                        monthlyFundingRateData.map((item, index) => {
                          return (
                            <div
                              key={index}
                              style={{
                                display: "flex",
                                alignItems: "center",
                                padding: "10px 0",
                              }}
                            >
                              <div
                                style={{
                                  width: "100px",
                                  fontSize: "13px",
                                  color: "#555",
                                  textAlign: "right",
                                  paddingRight: "12px",
                                }}
                              >
                                {item.category}
                              </div>
                              <div style={{ flex: 1, marginRight: "12px" }}>
                                <Progress
                                  percent={item.rate}
                                  showInfo={false}
                                  strokeColor="#7c522b"
                                  railColor="#f2eade"
                                  size={{ height: 10 }}
                                />
                              </div>
                              <div
                                style={{
                                  width: "65px",
                                  fontSize: "13px",
                                  fontWeight: 500,
                                  color: "#444",
                                  textAlign: "right",
                                }}
                              >
                                {item.rate}%
                              </div>
                            </div>
                          );
                        })
                      )}
                    </Col>
                  </Row>
                </Card>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
export default Report;
