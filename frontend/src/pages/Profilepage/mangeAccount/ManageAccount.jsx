import "./manageAccount.css";
import {
  apiGetAllAccounts,
  apiCreateAcc,
  apiUpdateAcc,
  apiSuspendAccount,
  apiActivateAccount,
  apiSearchAccounts,
} from "../../../api";

import { useLocation } from "react-router-dom";
import dayjs from "dayjs";
import close from "../../../assets/close.svg";
import { useEffect, useState } from "react";
import { PlusOutlined, LoadingOutlined } from "@ant-design/icons";
import {
  Button,
  DatePicker,
  Form,
  Upload,
  Space,
  Table,
  Tag,
  Input,
  message,
  Modal,
  Select,
} from "antd";

function ManageAccount() {
  const location = useLocation();
  const [createForm] = Form.useForm();
  const [updateForm] = Form.useForm();
  const [componentDisabled, setComponentDisabled] = useState(false);
  const [showcrea, setshowcrea] = useState(false);
  const [data, setdata] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState();
  const [inpValue, setinpvalue] = useState("");
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [setting, setsetting] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [updateValue, setupdateValue] = useState({});

  const uploadButton = (
    <button style={{ border: 0, background: "none" }} type="button">
      {loading ? <LoadingOutlined /> : <PlusOutlined />}
      <div style={{ marginTop: 8 }}>Upload</div>
    </button>
  );

  const normFile = (e) => {
    if (Array.isArray(e)) return e;
    return e?.fileList;
  };

  const columns = [
    {
      title: "Username",
      dataIndex: "username",
      key: "username",
      render: (text) => <span>{text}</span>,
    },
    {
      title: "Role",
      dataIndex: "role",
      key: "role",
    },
    {
      title: "Email",
      dataIndex: "email",
      key: "email",
      render: (text) => text || "—",
    },
    {
      title: "Phone",
      dataIndex: "phone",
      key: "phone",
      render: (text) => text || "—",
    },
    {
      title: "Dob",
      dataIndex: "dob",
      key: "dob",
      render: (text) => text || "—",
    },
    {
      title: "Status",
      key: "status",
      dataIndex: "status",
      render: (_, { status }) => (
        <Tag color={status === "online" ? "blue" : "default"}>
          {String(status || "offline").toUpperCase()}
        </Tag>
      ),
    },
    {
      title: "Access",
      key: "access",
      dataIndex: "access",
      render: (_, { access }) => (
        <Tag color={access === "active" ? "green" : "red"}>
          {String(access || "active").toUpperCase()}
        </Tag>
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="medium">
          <a
            onClick={() => {
              setshowcrea(true);
              setsetting("update");
              setupdateValue(record);
            }}
          >
            Update
          </a>
          {record.access === "active" ? (
            <a onClick={() => showModal(record)} style={{ color: "red" }}>
              Suspend
            </a>
          ) : (
            <a
              onClick={() => handleActivate(record)}
              style={{ color: "green" }}
            >
              Activate
            </a>
          )}
        </Space>
      ),
    },
  ];

  // Auto fill update form
  useEffect(() => {
    if (setting === "update" && updateValue && showcrea) {
      updateForm.setFieldsValue({
        email: updateValue.email,
        phone: updateValue.phone,
        role: updateValue.role,
        dob:
          updateValue.dob && updateValue.dob !== "None"
            ? dayjs(updateValue.dob)
            : null,
      });
    } else if (setting === "create") {
      createForm.resetFields();
      setImageUrl(null);
    }
  }, [updateValue, setting, showcrea, createForm, updateForm]);

  // Get all accounts
  const refresh = () => {
    try {
      apiGetAllAccounts()
        .then((res) => {
          if (res.accounts) {
            console.log(res);
            const user = res.accounts.map((item) => ({
              user_id: item.user_id,
              username: item.username,
              role: item.role,
              email: item.email || null,
              phone: item.phone || null,
              dob: item.dob || null,
              status: item.login_status,
              access: item.access,
              isActive: item.isActive,
            }));
            setdata(user);
          }
        })
        .catch((err) => console.log(err));
    } catch (error) {
      console.error("network:", error);
    }
  };

  useEffect(() => {
    refresh();
  }, []);

  const createAccount = () => {
    setshowcrea(!showcrea);
  };

  const showModal = (record) => {
    setSelectedUser(record);
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
    if (!selectedUser) return;
    try {
      apiSuspendAccount(selectedUser.user_id)
        .then((res) => {
          if (res.status === "success") {
            message.success(res.message);
            refresh();
          } else {
            message.error(res.error || "Failed to suspend");
          }
        })
        .catch(() => message.error("Network error"));
    } catch (error) {
      console.error("network:", error);
    }
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleActivate = (record) => {
    try {
      apiActivateAccount(record.user_id)
        .then((res) => {
          if (res.status === "success") {
            message.success(res.message);
            refresh();
          } else {
            message.error(res.error || "Failed to activate");
          }
        })
        .catch(() => message.error("Network error"));
    } catch (error) {
      console.error("network:", error);
    }
  };

  // One onFinish handles both create and update
  const onFinish = async (values) => {
    try {
      let res;
      if (setting === "create") {
        res = await apiCreateAcc({
          username: values.username,
          password: values.password,
          email: values.email || null,
          phone: values.phone || null,
          role: values.role,
          dob: values.dob ? values.dob.format("YYYY-MM-DD") : null,
        });
      } else {
        res = await apiUpdateAcc(Number(updateValue.user_id), {
          email: values.email && values.email !== "—" ? values.email : null,
          phone: values.phone && values.phone !== "—" ? values.phone : null,
          role: values.role || null,
          dob: values.dob ? values.dob.format("YYYY-MM-DD") : null,
          password: values.password || undefined,
        });
      }

      if (res.status === "success") {
        message.success(res.message);
        createForm.resetFields();
        updateForm.resetFields();
        setshowcrea(false);
        setImageUrl(null);
        refresh();
      } else {
        message.error(res.error || res.message || "Something went wrong");
      }
    } catch (error) {
      console.log(error);
    }
  };

  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
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

  const searchBut = () => {
    // if the input has value
    if (inpValue !== "") {
      try {
        apiGetAllAccounts({ username: inpValue })
          .then((res) => {
            if (res.accounts) {
              console.log(res);
              const user = res.accounts.map((item) => ({
                user_id: item.user_id,
                username: item.username,
                role: item.role,
                email: item.email || null,
                phone: item.phone || null,
                dob: item.dob || null,
                status: item.login_status,
                access: item.access,
                isActive: item.isActive,
              }));
              setdata(user);
            }
          })
          .catch((err) => console.log(err));
      } catch (error) {
        console.error("network:", error);
      }
    } else {
      // if the input value is empty
      setinpWarningVisi(true);
    }
  };

  return (
    <div className="ma">
      <div className="formhead">
        <li>
          <span>Username: </span>
          <input
            type="text"
            placeholder="Username"
            onChange={(e) => searchAccount(e)}
          />
          {inpWarningVisi ? (
            <span className="inpWarning">
              Please enter a username to search
            </span>
          ) : (
            ""
          )}
          <button onClick={() => searchBut()}>Search</button>
        </li>
        <span
          className="create"
          onClick={() => {
            createAccount();
            setsetting("create");
          }}
        >
          Create
        </span>
      </div>

      <Table columns={columns} dataSource={data} rowKey="user_id" />

      {/* CREATE FORM — all fields required */}
      {showcrea && setting === "create" ? (
        <div className="createForm">
          <img
            src={close}
            alt=""
            className="close"
            onClick={() => {
              setshowcrea(false);
              createForm.resetFields();
            }}
          />
          <div className="creForm">
            <span className="title">Create Account</span>
            <Form
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 13 }}
              layout="horizontal"
              disabled={componentDisabled}
              style={{ maxWidth: 600 }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
              form={createForm}
            >
              <Form.Item
                label="Username"
                name="username"
                rules={[{ required: true, message: "Please input username!" }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Password"
                name="password"
                rules={[{ required: true, message: "Please input password!" }]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                label="Role"
                name="role"
                rules={[{ required: true, message: "Please select a role!" }]}
              >
                <Select placeholder="Select role">
                  <Select.Option value="admin">Admin</Select.Option>
                  <Select.Option value="fund_raiser">Fund Raiser</Select.Option>
                  <Select.Option value="donee">Donee</Select.Option>
                  <Select.Option value="platform_manager">
                    Platform Manager
                  </Select.Option>
                </Select>
              </Form.Item>

              <Form.Item
                label="Email"
                name="email"
                rules={[{ required: true, message: "Please input email!" }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Phone"
                name="phone"
                rules={[{ required: true, message: "Please input phone!" }]}
              >
                <Input />
              </Form.Item>

              <Form.Item label="Date of Birth" name="dob">
                <DatePicker />
              </Form.Item>

              <Form.Item
                label="Avatar"
                name="avatar"
                valuePropName="fileList"
                getValueFromEvent={normFile}
              >
                <Upload
                  name="avatar"
                  listType="picture-circle"
                  className="avatar-uploader"
                  maxCount={1}
                  beforeUpload={() => false}
                >
                  {imageUrl ? (
                    <img
                      draggable={false}
                      src={imageUrl}
                      alt="avatar"
                      style={{ width: "100%" }}
                    />
                  ) : (
                    uploadButton
                  )}
                </Upload>
              </Form.Item>

              <Form.Item label={null} className="crebut">
                <Button htmlType="submit">Create</Button>
              </Form.Item>
            </Form>
          </div>
        </div>
      ) : null}

      {/* UPDATE FORM — all fields optional */}
      {showcrea && setting === "update" ? (
        <div className="createForm">
          <img
            src={close}
            alt=""
            className="close"
            onClick={() => {
              setshowcrea(false);
              updateForm.resetFields();
            }}
          />
          <div className="creForm">
            <span className="title">
              Update Account — {updateValue.username}
            </span>
            <Form
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 13 }}
              layout="horizontal"
              style={{ maxWidth: 600 }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
              form={updateForm}
            >
              <Form.Item label="Role" name="role">
                <Select placeholder="Select new role (optional)">
                  <Select.Option value="admin">Admin</Select.Option>
                  <Select.Option value="fund_raiser">Fund Raiser</Select.Option>
                  <Select.Option value="donee">Donee</Select.Option>
                  <Select.Option value="platform_manager">
                    Platform Manager
                  </Select.Option>
                </Select>
              </Form.Item>

              <Form.Item label="Email" name="email">
                <Input placeholder="Leave blank to keep current" />
              </Form.Item>

              <Form.Item label="Phone" name="phone">
                <Input placeholder="Leave blank to keep current" />
              </Form.Item>

              <Form.Item label="Date of Birth" name="dob">
                <DatePicker />
              </Form.Item>

              <Form.Item label="New Password" name="password">
                <Input.Password placeholder="Leave blank to keep current" />
              </Form.Item>

              <Form.Item
                label="Avatar"
                name="avatar"
                valuePropName="fileList"
                getValueFromEvent={normFile}
              >
                <Upload
                  name="avatar"
                  listType="picture-circle"
                  className="avatar-uploader"
                  maxCount={1}
                  beforeUpload={() => false}
                >
                  {imageUrl ? (
                    <img
                      draggable={false}
                      src={imageUrl}
                      alt="avatar"
                      style={{ width: "100%" }}
                    />
                  ) : (
                    uploadButton
                  )}
                </Upload>
              </Form.Item>

              <Form.Item label={null} className="crebut">
                <Button htmlType="submit">Update</Button>
              </Form.Item>
            </Form>
          </div>
        </div>
      ) : null}

      <Modal
        title="Suspension Confirmation"
        closable={{ "aria-label": "Custom Close Button" }}
        open={isModalOpen}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="Suspend"
        okType="danger"
      >
        <p>
          Are you sure you want to suspend <b>{selectedUser?.username}</b>?
        </p>
      </Modal>
    </div>
  );
}
export default ManageAccount;
