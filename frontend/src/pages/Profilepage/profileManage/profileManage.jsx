import { useLocation } from "react-router-dom";
import { useRef, useState } from "react";
// import fahh from "../../../assets/fahh.mp3";
import {
  apiGetAllProfiles,
  // apiProfileinfo,
  apiCreateProfile,
  apiEditProfile,
  apiSuspendProfile,
} from "../../../api";
import "../profileManage/profileManage.css";
import { Button, Checkbox, Form, Input, message, Modal } from "antd";
import { useEffect } from "react";
function profileManage() {
  const location = useLocation();
  const [profileData, setprofileData] = useState([]);
  const userdata = location.state?.userdata || {};
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [inpValue, setinpvalue] = useState("");
  const [creaVisi, setcreaVisi] = useState(false);
  const [buttype, setbuttype] = useState("");
  const { TextArea } = Input;
  const [form] = Form.useForm();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedRole, setSelectedRole] = useState("");

  const showModal = (id) => {
    setSelectedRole(id);
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
    try {
      console.log(selectedRole);
      apiSuspendProfile(selectedRole)
        .then((res) => {
          if (res.status == "success") {
            message.success(res.message);
            refresh();
          }
        })
        .catch((err) => {
          message.error(err.message);
        });
    } catch (error) {
      console.error("network:", error);
    }
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };
  const refresh = () => {
    try {
      apiGetAllProfiles({})
        .then((res) => {
          console.log(res);
          if (res.profiles) {
            const profile = res.profiles.map((item) => ({
              id: item.profile_id,
              role: item.profile_name,
              permission: item.permission,
              createDate: item.created_at,
              description: item.description,
              status: item.status,
            }));
            setprofileData(profile);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    } catch (error) {
      console.error("network:", error);
    }
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

  useEffect(() => {
    refresh();
  }, []);
  const searchPro = () => {
    // if the input has value
    if (inpValue !== "") {
      console.log(inpValue);
      try {
        apiGetAllProfiles({ query: inpValue })
          .then((res) => {
            if (res.profiles) {
              const profile = res.profiles.map((item) => ({
                id: item.profile_id,
                role: item.profile_name,
                createDate: item.created_at,
                description: item.description,
                status: item.status,
              }));
              setprofileData(profile);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      } catch (error) {
        console.error("network:", error);
      }
    } else {
      // if the input value is empty
      setinpWarningVisi(true);
    }
  };
  // status classname
  const getStatusClass = (item) => {
    if (item.status === "Disabled") {
      return "disabled";
    }
    if (item.role === "User Admin" || item.role === "Platform Manager") {
      return "status";
    }
    return "active";
  };

  const onFinish = (values) => {
    const payload = {
      profile_name: values.role,
      description: values.description,
    };
    console.log(values);
    try {
      if (buttype == "create") {
        apiCreateProfile(payload)
          .then((res) => {
            if (res.status == "success") {
              message.success(res.message);
              setcreaVisi(false);
              refresh();
            } else {
              message.error(res.message);
            }
          })
          .catch((err) => {
            console.log(err);
            const errorMsg = err.response?.data?.error || "Update failed";
            message.error(errorMsg);
          });
      } else if (buttype == "edit") {
        apiEditProfile(selectedRole, payload)
          .then((res) => {
            if (res.status == "success") {
              message.success(res.message);
              setcreaVisi(false);
              refresh();
            } else {
              message.error(res.message);
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    } catch (error) {
      console.error("network:", error);
    }
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  const editPro = (item) => {
    document.querySelector(".pmhead")?.scrollIntoView({ behavior: "smooth" });
    setbuttype("edit");
    setcreaVisi(true);
    setSelectedRole(item.id);
    form.setFieldsValue({
      role: item.role,

      description: item.description,
    });
  };
  return (
    <div className="pm">
      <div className="pmhead">
        <span className="title">User profiles</span>
        <li>
          <input
            type="text"
            placeholder="Username"
            onChange={(e) => {
              searchProfile(e);
            }}
          />
          <button onClick={searchPro}>Search</button>
          {inpWarningVisi ? (
            <span className="inpWarning">
              Please enter a username to search
            </span>
          ) : (
            ""
          )}
          <button
            className="creaPro"
            onClick={() => {
              setcreaVisi(!creaVisi);
              setbuttype("create");
              form.resetFields();
            }}
          >
            + Create new profile
          </button>
        </li>
      </div>
      <div className="profileContent">
        <div className={`createPro ${creaVisi ? "show" : ""}`}>
          <i onClick={() => setcreaVisi(false)}>X</i>
          <div className="createCard">
            <li>
              {buttype == "create"
                ? "Create Profile"
                : buttype == "edit"
                  ? "Edit"
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
                label="Role"
                name="role"
                rules={[{ required: true, message: "Please input role!" }]}
              >
                <Input />
              </Form.Item>

              {/* <Form.Item
                label="Permission"
                name="permission"
                rules={[
                  { required: true, message: "Please input permission!" },
                ]}
              >
                <Input />
              </Form.Item> */}
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
                  {buttype == "create"
                    ? "Create"
                    : buttype == "edit"
                      ? "Edit"
                      : ""}
                </Button>
              </Form.Item>
            </Form>
          </div>
        </div>

        {profileData.map((item) => {
          return (
            <div key={item.id} className="card">
              <li className="first">
                <div className="img">
                  {item.role === "admin"
                    ? "UA"
                    : item.role === "platform_manager"
                      ? "PM"
                      : item.role === "fund_raiser"
                        ? "FR"
                        : item.role === "donee"
                          ? "Donee"
                          : item.role.slice(0, 2).toUpperCase()}
                </div>
                <span className="role">{item.role}</span>
                <div className={getStatusClass(item)}>{item.status}</div>
              </li>
              <p>
                Creation date:{" "}
                {item.createDate ? item.createDate.slice(0, -3) : "N/A"}
              </p>
              <span>{item.description}</span>

              <li>
                <button onClick={() => editPro(item)}>Edit</button>
                <button onClick={() => showModal(item.id)}>Suspend</button>
              </li>
            </div>
          );
        })}
        <Modal
          title="Suspension Confirmation"
          closable={{ "aria-label": "Custom Close Button" }}
          open={isModalOpen}
          onOk={handleOk}
          onCancel={handleCancel}
          okText="Suspend"
          okType="danger"
        >
          <p>Are you sure you want to suspend this role?</p>
        </Modal>
      </div>
    </div>
  );
}
export default profileManage;
