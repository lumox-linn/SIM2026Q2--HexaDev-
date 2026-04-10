import "./manageAccount.css";
import { apiUserinfo, apiCreateAcc } from "../../../api";

import {
  useLocation,
  Outlet,
  Link,
  useParams,
  useNavigate,
} from "react-router-dom";

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
} from "antd";

function ManageAccount() {
  const location = useLocation();
  console.log(location);
  const [form] = Form.useForm();
  const [componentDisabled, setComponentDisabled] = useState(false);
  const [showcrea, setshowcrea] = useState(false);
  const [data, setdata] = useState([]);
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState();
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
      title: "Date of birth",
      dataIndex: "dob",
      key: "dob",
    },
    {
      title: "Activity",
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
          <a>Change {record.name}</a>
          <a>Delete</a>
        </Space>
      ),
    },
  ];
  // get info
  const refresh = () => {
    try {
      apiUserinfo({})
        .then((res) => {
          if (res.userdata) {
            console.log(res);
            const user = res.userdata.map((item) => ({
              username: item.username,
              password: item.password,
              role: item.role,
              email: item.email,
              phone: item.phone == undefined ? "None" : item.phone,
              status: item.activitystatus == "" ? "None" : item.activitystatus,
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
  };

  useEffect(() => {
    refresh();
  }, []);
  const createAccount = () => {
    setshowcrea(!showcrea);
  };
  const onFinish = async (values) => {
    const formData = new FormData();
    formData.append("username", values.username);
    formData.append("password", values.password);
    formData.append("email", values.email);
    formData.append("phone", values.phone);
    formData.append("age", values.age ? values.age.format("YYYY-MM-DD") : "");
    if (values.avatar && values.avatar.length > 0) {
      const fileBody = values.avatar[0].originFileObj;
      formData.append("avatar", fileBody);
    }

    try {
      const res = await apiCreateAcc(formData);
      if (res.status == "success") {
        message.open({
          type: "success",
          content: res.message,
        });
        form.resetFields();
        setshowcrea(false);
        refresh();
      } else if (res.status === "fail") {
        message.open({
          type: "error",
          content: res.message,
        });
        form.resetFields();
        return Promise.reject(new Error(res.message));
      }
    } catch (error) {
      console.log(error);
    }
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };

  return (
    <div className="ma">
      <div className="formhead">
        <li>
          <span>Username: </span>
          <input type="text" placeholder="Username" />
          <button>Search</button>
        </li>
        <span
          className="create"
          onClick={() => {
            createAccount();
          }}
        >
          Create
        </span>
      </div>
      <Table columns={columns} dataSource={data} rowKey="username" />
      {showcrea ? (
        <div className="createForm">
          <img
            src={close}
            alt=""
            className="close"
            onClick={() => {
              setshowcrea(false);
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
              form={form}
            >
              {/* <Form.Item label="Radio">
                <Radio.Group>
                  <Radio value="apple"> Apple </Radio>
                  <Radio value="pear"> Pear </Radio>
                </Radio.Group>
              </Form.Item> */}
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
                label="Age"
                name="age"
                rules={[
                  {
                    required: true,
                    message: "Please select your date of birth",
                  },
                ]}
              >
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
                <Button htmlType="submit">Create</Button>
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
