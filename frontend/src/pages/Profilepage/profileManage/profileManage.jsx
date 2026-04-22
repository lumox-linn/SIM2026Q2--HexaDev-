import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  apiProfileinfo,
  apiCreateProfile,
  apiEditProfile,
  apiSuspendProfile,
  apiActivateProfile,
} from "../../../api";
import "../profileManage/profileManage.css";
import { Button,Checkbox, Form, Input, message, Modal } from "antd";

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
  const [selectedProfile, setSelectedProfile] = useState(null); // ← CHANGE 1: store full profile not just role
  const [editValue, setEditValue] = useState(null);

  // ← CHANGE 2: showModal stores full profile object
  const showModal = (profile) => {
    setSelectedProfile(profile);
    setIsModalOpen(true);
  };

  // ← CHANGE 3: handleOk uses profile_id not role
  const handleOk = () => {
    setIsModalOpen(false);
    if (!selectedProfile) return;
    try {
      apiSuspendProfile(selectedProfile.id)
        .then((res) => {
          if (res.status === "success") {
            message.success(res.message);
            refresh();
          } else {
            message.error(res.error || "Failed to suspend");
          }
        })
        .catch((err) => {
          message.error("Network error");
        });
    } catch (error) {
      console.error("network:", error);
    }
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  // ← CHANGE 4: handleActivate for reactivating profiles
  const handleActivate = (profile) => {
    try {
      apiActivateProfile(profile.id)
        .then((res) => {
          if (res.status === "success") {
            message.success(res.message);
            refresh();
          } else {
            message.error(res.error || "Failed to activate");
          }
        })
        .catch((err) => {
          message.error("Network error");
        });
    } catch (error) {
      console.error("network:", error);
    }
  };

  // ← CHANGE 5: refresh uses res.profiles not res.profiledata
  const refresh = () => {
    try {
      apiProfileinfo()
        .then((res) => {
          console.log(res);
          if (res.profiles) {
            const profile = res.profiles.map((item) => ({
              id:          item.profile_id,      // ← profile_id not proid
              role:        item.profile_name,    // ← profile_name not role
              description: item.description,
              status:      item.status,
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

  // ← CHANGE 6: searchPro uses query param not username
  const searchPro = () => {
    // if the input has value
    if (inpValue !== "") {
      console.log(inpValue);
      try {
        apiProfileinfo({ query: inpValue })
          .then((res) => {
            if (res.profiles) {
              const profile = res.profiles.map((item) => ({
                id:          item.profile_id,
                role:        item.profile_name,
                description: item.description,
                status:      item.status,
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

  const getStatusClass = (item) => {
    if (item.status === "suspended") return "disabled";
    return "active";
  };

  // ← CHANGE 7: onFinish uses correct API and field names
  const onFinish = (values) => {
    try {
      if (buttype === "create") {
        apiCreateProfile({
          profile_name: values.role,           // ← profile_name not role
          description:  values.description,
        })
          .then((res) => {
            if (res.status === "success") {
              message.success(res.message);
              setcreaVisi(false);
              form.resetFields();
              refresh();
            } else {
              message.error(res.error || res.message);
            }
          })
          .catch((err) => console.log(err));
      } else if (buttype === "edit") {
        // ← CHANGE 8: edit uses profile_id
        apiEditProfile(editValue.id, {
          profile_name: values.role,
          description:  values.description,
        })
          .then((res) => {
            if (res.status === "success") {
              message.success(res.message);
              setcreaVisi(false);
              form.resetFields();
              refresh();
            } else {
              message.error(res.error || res.message);
            }
          })
          .catch((err) => console.log(err));
      }
    } catch (error) {
      console.error("network:", error);
    }
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  // ← CHANGE 9: editPro stores full item for profile_id
  const editPro = (item) => {
    setbuttype("edit");
    setEditValue(item);
    setcreaVisi(true);
    form.setFieldsValue({
      role:        item.role,
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
            placeholder="Search profile..."
            onChange={(e) => searchProfile(e)}
          />
          <button onClick={searchPro}>Search</button>
          {inpWarningVisi ? (
            <span className="inpWarning">Please enter a name to search</span>
          ) : ("")}
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
              {buttype === "create" ? "Create Profile" : buttype === "edit" ? "Edit Profile" : ""}
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
                label="Profile Name"
                name="role"
                rules={[{ required: true, message: "Please input profile name!" }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Description"
                name="description"
                rules={[{ required: true, message: "Please input description!" }]}
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

        {profileData.map((item) => {
          return (
            <div key={item.id} className="card">
              <li className="first">
                <div className="img">
                  {item.role === "admin" ? "UA"
                    : item.role === "platform_manager" ? "PM"
                    : item.role === "fund_raiser" ? "FR"
                    : item.role === "donee" ? "DO"
                    : item.role.substring(0, 2).toUpperCase()}
                </div>
                <span className="role">{item.role}</span>
                {/* ← CHANGE 10: status tag color based on value */}
                <div className={getStatusClass(item)}>
                  {item.status === "active" ? "Active" : "Suspended"}
                </div>
              </li>

              <span>{item.description}</span>

              <li>
                <button onClick={() => editPro(item)}>Edit</button>
                {/* ← CHANGE 11: show Suspend or Activate based on status */}
                {item.status === "active" ? (
                  <button onClick={() => showModal(item)}>Suspend</button>
                ) : (
                  <button onClick={() => handleActivate(item)} style={{ color: "green" }}>
                    Activate
                  </button>
                )}
                <Modal
                  title="Suspension Confirmation"
                  open={isModalOpen}
                  onOk={handleOk}
                  onCancel={handleCancel}
                  okText="Suspend"
                  okType="danger"
                >
                  <p>Are you sure you want to suspend <b>{selectedProfile?.role}</b>? All associated accounts will also be suspended.</p>
                </Modal>
              </li>
            </div>
          );
        })}
      </div>
    </div>
  );
}
export default profileManage;