import "./ActivityStatus.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import dayjs from "dayjs";
import eye from "../../../assets/eye.svg";
import iconheart from "../../../assets/iconheart.svg";
import {
  apiGetAllActivities,
  apiCreateActivities,
  apiEditActivities,
  apiSuspendActivities,
  apiSearchAcHis,
  apiBrowseCategories,
} from "../../../api";
import { createStaticStyles } from "antd-style";
import restart from "../../../assets/restart.svg";
import {
  Button,
  Checkbox,
  ConfigProvider,
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
  const [startDate, setStartDate] = useState(null);
  const location = useLocation();
  const [activityData, setactivityData] = useState([]);
  const userdata = location.state?.userdata || {};
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const userId = localStorage.getItem("userData")
    ? JSON.parse(localStorage.getItem("userData")).userid
    : null;
  const [allcat, setallcat] = useState([]);
  const [selectv, setselectv] = useState(null);
  const [inpValue, setinpvalue] = useState("");
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
  const [catid, setcatid] = useState(0);
  // // const [cat, setcat] = useState(null);
  // const [allcategories, setallCategories] = useState([
  //   { category: "Animal", catId: 2 },
  //   { category: "Education", catId: 3 },
  //   { category: "Environment", catId: 5 },
  //   { category: "Health", catId: 4 },
  //   { category: "School", catId: 1 },
  // ]);

  // ✅ Start empty
  const [allcategories, setallCategories] = useState([]);

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
    try {
      apiSuspendActivities(selectedActivities.activity_id)
        .then((res) => {
          console.log(res);
          if (res.status === "success") {
            message.success(res.message);
            refresh();
          } else {
            message.error(res.error || "Failed to suspend");
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
  const refresh = () => {
    console.log(userId);
    try {
      apiGetAllActivities({ user_id: userId })
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
              start_date: item.start_date,
              // start_date: item.start_date.split(" ").slice(0, 4).join(" "),
              end_date: item.end_date,
              view_count: item.view_count,

              shortlist_count: item.shortlist_count,

              // end_date: item.end_date.split(" ").slice(0, 4).join(" "),
            }));
            setactivityData(activities);

            const uniqueCategoryNamess = [
              ...new Set(
                activities.map((item) => item.category_name).filter(Boolean),
              ),
            ];

            const selectOptions = uniqueCategoryNamess.map((name) => ({
              value: name,
              label: name,
            }));
            setallcat(selectOptions);
            console.log(selectOptions);
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
   
    apiBrowseCategories()
      .then((res) => {
        if (res.categories) {
          const cats = res.categories
            .filter(c => c.status === 'active')
            .map(c => ({ category: c.category_name, catId: c.category_id }));
          setallCategories(cats);
        }
      })
      .catch ((err) => console.log(err));
}, []);
const [endDate, setEndDate] = useState(null);
const searchPro = () => {
  // if the input has value
  if (inpValue !== "") {
    console.log(inpValue);
    try {
      apiGetAllActivities({ query: inpValue })
        .then((res) => {
          console.log(res);
          if (res.categories) {
            const cats = res.categories
              .filter(c => c.status === 'active')
              .map(c => ({
                category: c.category_name,
                catId: c.category_id,
              }));
            setallCategories(cats);
          }
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
              start_date: item.start_date,
              // start_date: item.start_date.split(" ").slice(0, 4).join(" "),
              end_date: item.end_date,
            }));
            setactivityData(activities);
          }
        })
        .catch((err) => {
          setactivityData([]);
          message.error(err.response?.data?.error);
        });
    } catch (error) {
      message.error(error.response?.data?.error);
    }
  } else {
    // if the input value is empty
    setinpWarningVisi(true);
  }
  if (selectv || (startDate && endDate)) {
    setinpWarningVisi(false);
    try {
      apiSearchAcHis(
        selectv
          ? { category_id: catid }
          : { start_date: startDate, end_Date: endDate },
      )
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.log(err);
          message.error(err.response?.data?.error);
        });
    } catch (error) {
      console.log(error);
      message.error(error.response?.data?.error);
    }
  }
};

const getStatusClass = (item) => {
  if (item.status === "suspended") return "disabled";
  return "active";
};

const onFinish = (values) => {
  // const pp = allcategories.find(
  //   (item) => item.category == values.category_id,
  // );
  // console.log(pp);
  const cat = allcategories.find(
    (item) => item.category == values.category_id,
  );
  console.log(values);
  try {
    if (buttype === "create") {
      console.log(values);
      apiCreateActivities({
        title: values.title,
        description: values.description,
        category_id: cat.catId,
        created_by: userId,
        target_amount: values.target_amount,
        start_date: values.start_date
          ? values.start_date.format("YYYY-MM-DD")
          : null,
        end_date: values.end_date
          ? values.end_date.format("YYYY-MM-DD")
          : null,
      })
        .then((res) => {
          console.log(res);
          if (res.status === "success") {
            message.success(res.message);
            setcreaVisi(false);
            form.resetFields();
            refresh();
          } else {
            message.error(res.error || res.message);
          }
        })
        .catch((err) => message.error(err.response?.data?.error));
    } else if (buttype === "edit") {
      console.log("edit");
      console.log(cat);
      apiEditActivities(Number(editValue.activity_id), {
        title: values.title,
        description: values.description,
        category_id: cat ? cat.catId : null,
        created_by: userId,
        amount_raised: values.amount_raised,
        target_amount: values.target_amount,
        start_date: values.start_date
          ? values.start_date.format("YYYY-MM-DD")
          : null,
        end_date: values.end_date
          ? values.end_date.format("YYYY-MM-DD")
          : null,
      })
        .then((res) => {
          console.log(res);
          if (res.status === "success") {
            message.success(res.message);
            setcreaVisi(false);
            form.resetFields();
            refresh();
          } else {
            message.error(res.error || res.message);
          }
        })
        .catch((err) => {
          message.error(err.response?.data?.error);
        });
    }
  } catch (error) {
    message.error(error.response?.data?.error);
    console.log(error);
  }
};

const onFinishFailed = (errorInfo) => {
  console.log("Failed:", errorInfo);
};

const editPro = (item) => {
  document.querySelector(".pmhead")?.scrollIntoView({ behavior: "smooth" });
  setbuttype("edit");
  console.log(item);
  setEditValue(item);
  setViewActivity({ actId: null, viewstatus: false });
  console.log(allcategories);
  const found = allcategories.find(
    (i) => i.category?.toLowerCase() === item.category_name?.toLowerCase(),
  );

  // console.log(item);
  setcreaVisi(true);
  console.log(found);
  setTimeout(() => {
    form.setFieldsValue({
      title: item.title,
      description: item.description,
      category_id: found?.category || null,
      created_by: item.creator,
      target_amount: item.target_amount,
      start_date: item.start_date ? dayjs(item.start_date) : null,
      amount_raised: item.amount_raised,
      end_date: item.end_date ? dayjs(item.end_date) : null,
    });
  }, 100);
};
return (
  <div className="mc">
    <div className="pmhead">
      <span className="title">Activity management</span>
      <li>
        <input
          type="text"
          placeholder="Search Activities..."
          onChange={(e) => searchActivities(e)}
          disabled={selectv !== null || startDate !== null ? true : false}
        />

        {inpWarningVisi ? (
          <span className="inpWarning">
            Please enter a activity to search
          </span>
        ) : (
          ""
        )}
        <span style={{ fontSize: "14px", marginLeft: "10px" }}>
          Fundraising history:
        </span>
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
            apiGetAllActivities({ user_id: userId })
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
                // message.error(err.response?.data?.error);
              });
          }}
          options={allcat}
        />
        <img
          src={restart}
          alt=""
          className="restart"
          style={{ width: "20px" }}
          onClick={() => {
            setStartDate(null);

            setselectv(undefined);
            setinpWarningVisi(false);
            refresh();
          }}
        />
        <button onClick={searchPro}>Search</button>

        <button
          className="creaPro"
          onClick={() => {
            setcreaVisi(!creaVisi);
            setbuttype("create");
            form.resetFields();
            if (viewActivity.viewstatus) {
              setViewActivity({ actId: null, viewstatus: false });
            }
          }}
        >
          + Create New Activity
        </button>
      </li>
    </div>

    <div className="profileContent">
      <div className={`createPro ${creaVisi ? "show" : ""}`}>
        <i onClick={() => setcreaVisi(false)}>X</i>
        <div className="createCard">
          <li>
            {buttype === "create"
              ? "Create Activities"
              : buttype === "edit"
                ? "Edit Activities"
                : ""}
          </li>
          <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 18 }}
            style={{ maxWidth: 600 }}
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
            form={form}
          >
            <Form.Item
              label="Activities Title"
              name="title"
              rules={[
                { required: true, message: "Please input Activities title!" },
              ]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="Target Amount"
              name="target_amount"
              rules={[
                { required: true, message: "Please input target amount!" },
                {
                  transform: (value) => Number(value),
                  type: "number",
                  message: "Please input a valid number!",
                },
              ]}
              style={{ position: "relative" }}
            >
              <Input />
            </Form.Item>
            {buttype === "edit" ? (
              <Form.Item
                label="Amount Raised"
                name="amount_raised"
                rules={[
                  { required: true, message: "Please input raised amount!" },
                  {
                    transform: (value) => Number(value),
                    type: "number",
                    message: "Please input a valid number!",
                  },
                ]}
                style={{ position: "relative" }}
              >
                <Input />
              </Form.Item>
            ) : null}

            <Form.Item label="Category" name="category_id">
              <Select
                rules={[{ required: true, message: "Please input!" }]}
                options={allcategories.map((element, index) => ({
                  value: element.category,
                  label: element.category,
                  key: element.catId,
                }))}
              />
            </Form.Item>

            <Form.Item label="Start Date" name="start_date">
              <DatePicker />
            </Form.Item>
            <Form.Item label="End Date" name="end_date">
              <DatePicker />
            </Form.Item>
            <Form.Item
              label="Description"
              name="description"
              rules={[
                { required: true, message: "Please input description!" },
              ]}
            >
              <TextArea rows={3} />
            </Form.Item>

            <Form.Item label={null}>
              <Button type="primary" htmlType="submit">
                {buttype === "create" ? "Create" : "Save"}
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>

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
                      {item.category}
                    </Tag>
                  </p>
                ) : null}
                <span
                  style={{
                    position: "absolute",
                    right: "70px",
                    display: "flex",
                    flexDirection: "center",
                    gap: 10,
                  }}
                >
                  <img src={iconheart} alt="" style={{ width: "20px" }} />
                  {item.shortlist_count}
                </span>
                <span
                  style={{
                    position: "absolute",
                    right: "20px",
                    display: "flex",
                    flexDirection: "center",
                    gap: 10,
                  }}
                >
                  <img src={eye} alt="" style={{ width: "20px" }} />
                  {item.view_count}
                </span>
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
                <button onClick={() => editPro(item)}>Edit</button>
                <button onClick={() => showModal(item)}>Delete</button>

                {/* {item.status === "active" ? (
                    <button onClick={() => showModal(item)}>Suspend</button>
                  ) : (
                    <button
                      onClick={() => handleActivate(item)}
                      className="activeBut"
                    >
                      Activity
                    </button>
                  )} */}
                {viewActivity.actId == item.activity_id ? null : (
                  <button
                    onClick={() => {
                      viewAct(item);
                      if (creaVisi) {
                        setcreaVisi(!creaVisi);
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
