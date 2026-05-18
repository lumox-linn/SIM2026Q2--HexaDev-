import "../Activities/activities.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { createStaticStyles } from "antd-style";
import {
  apiGetDoneeActivities,
  apiSaveFavourite,
  apiViewActivity,
  apisearchActivities,
  apiBrowseCategories,
} from "../../api";
import heart from "../../assets/heart.svg";
import {
  message,
  Flex,
  Tag,
  Progress,
  Select,
} from "antd";
import { CheckCircleOutlined, CloseCircleOutlined } from "@ant-design/icons";

function ActivityStatus() {
  const location  = useLocation();
  const userId    = localStorage.getItem("userData")
    ? JSON.parse(localStorage.getItem("userData")).userid
    : null;

  const [activityData, setactivityData]   = useState([]);
  const [allActivities, setAllActivities] = useState([]); // ✅ full list for filter reset
  const [allcat, setallcat]               = useState([]);
  const [inpValue, setinpvalue]           = useState("");
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [viewActivity, setViewActivity]   = useState({ viewstatus: false, actId: null });

  // ── Helpers ───────────────────────────────────────────────
  const getStatusClass = (item) =>
    item.status === "suspended" ? "disabled" : "active";

  const percentage = (item) => {
    const raised = parseFloat(item.amount_raised) || 0;
    const target = parseFloat(item.target_amount) || 0;
    if (target <= 0) return 0;
    return Math.round((raised / target) * 100);
  };

  const progressClass = {
    root: "demo-progress-root",
    rail: "demo-progress-rail",
    track: "demo-progress-track",
  };

  const styles = {
    root: { backgroundColor: "#e6f7ff", borderRadius: "10px" },
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

  const onSearch = (value) => console.log("search:", value);

  // ── Map backend items ─────────────────────────────────────
  const mapActivities = (list) =>
    list.map((item) => ({
      activity_id:   item.activity_id,
      title:         item.title,
      description:   item.description,
      amount_raised: item.amount_raised,
      category:      item.category_name,
      category_name: item.category_name,
      status:        item.status,
      created_at:    item.created_at?.split(" ").slice(0, 4).join(" "),
      creator:       item.creator,
      target_amount: item.target_amount,
      start_date:    item.start_date?.split(" ").slice(0, 4).join(" "),
      end_date:      item.end_date?.split(" ").slice(0, 4).join(" "),
    }));

  // ── Refresh ───────────────────────────────────────────────
  const refresh = () => {
    apiGetDoneeActivities()
      .then((res) => {
        if (res.activities) {
          const activities = mapActivities(res.activities);
          setactivityData(activities);
          setAllActivities(activities); // ✅ keep full copy
        }
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    refresh();

    // ✅ fetch ALL active categories from DB — not derived from activities
    apiBrowseCategories()
      .then((res) => {
        if (res.categories) {
          setallcat(
            res.categories
              .filter(c => c.status === "active")
              .map(c => ({ value: c.category_name, label: c.category_name }))
          );
        }
      })
      .catch((err) => console.log(err));
  }, []);

  // ── Search by title ───────────────────────────────────────
  const searchActivities = (e) => {
    setinpvalue(e.target.value);
    if (e.target.value !== "") setinpWarningVisi(false);
    else refresh();
  };

  const searchPro = () => {
    if (inpValue !== "") {
      apisearchActivities({ query: inpValue })
        .then((res) => {
          if (res.activities) {
            setactivityData(mapActivities(res.activities));
          }
        })
        .catch((err) => message.error(err.response?.data?.error));
    } else {
      setinpWarningVisi(true);
    }
  };

  // ── Category filter ✅ filter() not find() ────────────────
  const onChange = (value) => {
    if (value) {
      // ✅ filter shows ALL activities in that category
      const filtered = allActivities.filter(
        (item) => item.category_name === value
      );
      setactivityData(filtered);
    } else {
      // ✅ clear → restore full list
      setactivityData(allActivities);
    }
  };

  // ── View + Save ───────────────────────────────────────────
  const viewAct = (item) => {
    setViewActivity({ viewstatus: true, actId: item.activity_id });
    window.scrollTo({ top: 0, behavior: "smooth" });
    apiViewActivity(item.activity_id)
      .then((res) => console.log(res))
      .catch((err) => message.error(err.response?.data?.error));
  };

  const saveAct = (item) => {
    apiSaveFavourite(item.activity_id)
      .then((res) => {
        if (res.status === "success") message.success(res.message);
      })
      .catch((err) => message.error(err.response?.data?.error));
  };

  return (
    <div className="mc">
      <div className="pmhead">
        <span className="title">Browse fundraising activities</span>
        <li>
          <input
            type="text"
            placeholder="Search Activities..."
            onChange={searchActivities}
          />
          <button onClick={searchPro} className="searchb">Search</button>
          {inpWarningVisi && (
            <span className="inpWarning">Please enter an activity to search</span>
          )}
          {/* ✅ shows all DB categories, not just ones with activities */}
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
          .map((item) => (
            <div
              key={item.activity_id}
              className={item.activity_id === viewActivity.actId ? "cardView" : "card"}
            >
              {item.activity_id === viewActivity.actId && (
                <i
                  onClick={() => setViewActivity({ actId: null, viewstatus: false })}
                  className="closeView"
                >
                  X
                </i>
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
                    icon={item.status === "active"
                      ? <CheckCircleOutlined />
                      : <CloseCircleOutlined />}
                  >
                    {item.category}
                  </Tag>
                </p>
                <button className="save" onClick={() => saveAct(item)}>Save</button>
              </li>

              {item.activity_id === viewActivity.actId && (
                <li className="date">
                  <p>
                    <span>Start date: {item.start_date ?? "—"}</span>
                    <span style={{ marginLeft: "30px", color: "#eb2f2f" }}>
                      End date: {item.end_date ?? "—"}
                    </span>
                  </p>
                  <p style={{ width: "100%", height: "20px", display: "flex", justifyContent: "space-between" }}>
                    <span style={{ color: "#6bacea" }}>Target: ${item.target_amount}</span>
                    <span style={{ color: "#b3bc4b" }}>Raised: ${item.amount_raised}</span>
                  </p>
                  <Flex vertical gap="large">
                    <Progress classNames={progressClass} styles={stylesFn} percent={percentage(item)} />
                  </Flex>
                </li>
              )}

              <span style={{ marginBottom: "45px" }}>{item.description}</span>

              <li className="butStyle" style={{ position: "absolute", bottom: "13px", zIndex: 10, left: "19px" }}>
                <button className="donate">
                  <img src={heart} alt="" className="heart" />
                  Donate
                </button>

                {viewActivity.actId !== item.activity_id && (
                  <button onClick={() => viewAct(item)}>View</button>
                )}
              </li>
            </div>
          ))}
      </div>
    </div>
  );
}

export default ActivityStatus;