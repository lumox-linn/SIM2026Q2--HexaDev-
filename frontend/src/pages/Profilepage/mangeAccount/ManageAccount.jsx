import "./manageAccount.css";
import { apiUserinfo, apiCreateAcc, apiUpdateAcc } from "../../../api";

import { useLocation } from "react-router-dom";

import close from "../../../assets/close.svg";
import { use, useEffect, useState } from "react";
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
} from "antd";

function ManageAccount() {
  const location = useLocation();
  const [form] = Form.useForm();
  const [componentDisabled, setComponentDisabled] = useState(false);
  const [showcrea, setshowcrea] = useState(false);
  const [data, setdata] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState();
  const [inpValue, setinpvalue] = useState("");
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [setting, setsetting] = useState("");

  const handleChange = (info) => {
    if (info.file.status === "uploading") {
      setLoading(true);
      return;
    }
    if (info.file.status === "done") {
      // Get this url from response in real world.
      getBase64(info.file.originFileObj, (url) => {
        setLoading(false);
        setImageUrl(url);
      });
    }
  };
  const uploadButton = (
    <button style={{ border: 0, background: "none" }} type="button">
      {loading ? <LoadingOutlined /> : <PlusOutlined />}
      <div style={{ marginTop: 8 }}>Upload</div>
    </button>
  );
  const normFile = (e) => {
    if (Array.isArray(e)) {
      return e;
    }
    return e?.fileList;
  };
  const [updateValue, setupdateValue] = useState({});
  const columns = [
    {
      title: "Username",
      dataIndex: "username",
      key: "username",
      render: (text) => <span>{text}</span>,
    },
    {
      title: "Password",
      dataIndex: "password",
      key: "password",
      render: (text) => (
        <Input.Password
          value={text}
          readOnly
          variant={false}
          style={{ width: 150 }}
        />
      ),
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
    },
    {
      title: "Phone",
      dataIndex: "phone",
      key: "phone",
    },
    {
      title: "Dob",
      dataIndex: "dob",
      key: "dob",
    },

    {
      title: "Stutus",
      key: "status",
      dataIndex: "status",
      render: (_, { status }) => (
        <Tag color="green" key={status}>
          {String(status).toUpperCase()}
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
            Update {record.name}
          </a>
          <a onClick={() => console.log("current：", record)}>Suspend</a>
        </Space>
      ),
    },
  ];
  // update user account
  useEffect(() => {
    if (setting === "update" && updateValue && showcrea) {
      // when update the value automatically appear
      form.setFieldsValue({
        username: updateValue.username,
        password: updateValue.password,
        email: updateValue.email,
        phone: updateValue.phone,
        avatar: updateValue.avatar,
      });
      if (updateValue.avatar && updateValue.avatar !== "None") {
        setImageUrl(updateValue.avatar);
        form.setFieldsValue({
          avatar: [
            {
              uid: "-1",
              name: "image.png",
              status: "done",
              url: updateValue.avatar,
            },
          ],
        });
      } else {
        setImageUrl(null);
        form.setFieldsValue({ avatar: [] });
      }
    } else if (setting === "create") {
      form.resetFields(); // clear the value
      setImageUrl(null);
    }
  }, [updateValue, setting, showcrea, form]);
  // get info
  const refresh = () => {
    try {
      apiUserinfo({})
        .then((res) => {
          if (res.userdata) {
            const user = res.userdata.map((item) => ({
              username: item.username,
              password: item.password,
              role: item.role,
              email: item.email,
              phone: item.phone == undefined ? "None" : item.phone,
              status: item.loginstatus,
              dob: item.dob == "" ? "None" : item.dob,
              avatar: item.useravatar,
            }));
            setdata(user);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    } catch (error) {
      console.error("network:", error);
    }
  };

  useEffect(() => {
    refresh();
  }, []);
  // show creating account page
  const createAccount = () => {
    setshowcrea(!showcrea);
  };
  const onFinish = async (values) => {
    const formData = new FormData();
    formData.append("username", values.username);
    formData.append("password", values.password);
    formData.append("email", values.email);
    formData.append("phone", values.phone);

    if (values.avatar && values.avatar.length > 0) {
      const fileBody = values.avatar[0].originFileObj;
      formData.append("avatar", fileBody);
    }

    try {
      let res;
      if (setting === "create") {
        res = await apiCreateAcc(formData);
      } else {
        res = await apiUpdateAcc(formData);
      }
      if (res.status === "success") {
        message.success(res.message);
        form.resetFields();
        setshowcrea(false);
        setImageUrl(null);
        refresh();
      } else {
        message.error(res.message);
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
        apiUserinfo({ username: inpValue })
          .then((res) => {
            if (res.userdata) {
              console.log(res);
              const user = res.userdata.map((item) => ({
                username: item.username,
                password: item.password,
                role: item.role,
                email: item.email,
                dob: item.dob,
                phone: item.phone == undefined ? "None" : item.phone,
                status:
                  item.activitystatus == "" ? "None" : item.activitystatus,
                dob: item.dob == "" ? "None" : item.dob,
              }));
              setdata(user);
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

  return (
    <div className="ma">
      <div className="formhead">
        <li>
          <span>Username: </span>

          <input
            type="text"
            placeholder="Username"
            onChange={(e) => {
              searchAccount(e);
            }}
          />
          {inpWarningVisi ? (
            <span className="inpWarning">
              Please enter a username to search
            </span>
          ) : (
            ""
          )}

          <button
            onClick={() => {
              searchBut();
            }}
          >
            Search
          </button>
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
      <Table
        columns={columns}
        dataSource={data}
        rowKey="username"
        // rowClassName={(record, index) => {
        //   return index === 0 ? "first-row-black" : "";
        // }}
      />
      {showcrea ? (
        <div className="createForm">
          <img
            src={close}
            alt=""
            className="close"
            onClick={() => {
              setshowcrea(false);
              form.resetFields();
            }}
          />
          <div className="creForm">
            <span className="title">
              {setting === "create" ? "Create Account" : "Update Account"}
            </span>

            <Form
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 13 }}
              layout="horizontal"
              disabled={componentDisabled}
              style={{ maxWidth: 600 }}
              onFinish={onFinish}
              onFinishFailed={onFinishFailed}
              autoComplete="off"
              form={form}
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
                <Input />
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
                rules={[
                  { required: true, message: "Please input phone number!" },
                ]}
              >
                <Input />
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
                  // onChange={handleChange}
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
                <Button htmlType="submit">
                  {setting === "create" ? "Create" : "Update"}
                </Button>
              </Form.Item>
            </Form>
          </div>
        </div>
      ) : (
        ""
      )}
    </div>
  );
}
export default ManageAccount;
