import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Checkbox, Form, Input, message, Select } from "antd";
import { ArrowLeftOutlined } from "@ant-design/icons";
import "../Login/login.css";
import { apiLogin, apiRegister, apiSendCode } from "../../api";

function Login() {
  const [form] = Form.useForm();
  const [register, setregister] = useState(false);
  const [show, setshow] = useState(false);
  const [codeable, setcodeable] = useState(false);
  const [time, settime] = useState(30);
  const [loginstatus, setloginstatus] = useState(false);
  const navigate = useNavigate();
  const handleSendCode = async () => {
    try {
      // get value from the form
      const email = form.getFieldValue("email");

      if (
        !email ||
        !/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(email)
      ) {
        alert("Please enter a valid email address!");
        return;
      } else {
        setcodeable(true);
      }

      //call api
      const res = await apiSendCode({ email });

      if (res.status === "success") {
        console.log("Varification code sent:", email);
      } else {
        alert(res.message || "Send failed");
      }
    } catch (err) {
      console.error("network:", err);
    }
  };
  const onFinish = async (values) => {
    console.log(values);
    try {
      if (!register) {
        const res = await apiLogin(values);
        if (res.status == "success") {
          localStorage.setItem(
            "userData",
            JSON.stringify(res.userdata),
            // avatarstatus,
          );
          window.dispatchEvent(new Event("storage"));
          message.open({
            type: "success",
            content: res.message,
          });
          setTimeout(() => {
            navigate("/home", {
              state: {
                userdata: res.userdata,
                fromLogin: true,
              },
            });
          }, 1000);
        } else if (res.status === "fail") {
          setshow(true);
          return Promise.reject(new Error(res.message || "login failed"));
        }
      } else {
        const reg = await apiRegister(values);

        if (reg.status == "success") {
          console.log("get", reg);

          message.open({
            type: "success",
            content: reg.message,
          });
          setTimeout(() => {
            setregister(false);
            navigate("/login");
          }, 1000);
        } else if (reg.status === "fail") {
          return Promise.reject(new Error(reg.message || "register failed"));
        }
      }
    } catch (err) {
      console.log(err);
    }
  };
  useEffect(() => {
    let interval = null;
    if (codeable && time > 0) {
      interval = setInterval(() => {
        settime((prev) => prev - 1);
      }, 1000);
    } else if (time === 0) {
      setcodeable(false);
      settime(30);
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [codeable, time]);
  const handleChange = (value) => {
    console.log(`selected ${value}`);
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  return (
    <div className="login">
      <div className="loginbox">
        {register == true ? (
          <ArrowLeftOutlined
            onClick={() => {
              setregister(false);
            }}
          />
        ) : (
          ""
        )}

        <span className="companyname">CompanyName</span>
        {register == false ? (
          <Form
            form={form}
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 20 }}
            style={{ maxWidth: 600, width: "100%" }}
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item
              label="Username"
              name="username"
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <Input className="username" placeholder="username" />
            </Form.Item>

            <Form.Item
              label="Password"
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password className="password" placeholder="Password" />
            </Form.Item>
            {show == true ? (
              <li className="wrongpass">Username or password wrong</li>
            ) : (
              <li></li>
            )}
            <Form.Item
              name="Identity"
              rules={[{ required: true, message: "Please select a identity" }]}
              label="Identity"
            >
              <Select
                style={{ width: 200 }}
                onChange={handleChange}
                rules={[{ required: true, message: "Province is required" }]}
                placeholder="Choose your identity"
                options={[
                  { label: <span>User admin</span>, value: "User Admin" },
                  { label: <span>Doner</span>, value: "Doner" },
                  {
                    label: <span>Platform manager</span>,
                    value: "Platform Manager",
                  },
                ]}
              />
            </Form.Item>

            <Form.Item name="remember" valuePropName="checked" label={null}>
              <Checkbox>Remember me</Checkbox>
            </Form.Item>

            <Form.Item label={null}>
              <Button htmlType="submit" color="cyan" variant="filled">
                Login
              </Button>
            </Form.Item>
            <li className="set">
              <span
                onClick={() => {
                  setregister(true);
                  setshow(false);
                }}
              >
                Create account
              </span>
              <span>Forget password</span>
            </li>
          </Form>
        ) : (
          <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 20 }}
            style={{ maxWidth: 600, width: "100%" }}
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
            autoComplete="off"
          >
            <Form.Item
              label="Username"
              name="regusername"
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <Input className="regusername" placeholder="Username" />
            </Form.Item>
            <Form.Item
              label="Email"
              name="email"
              rules={[{ required: true, message: "Please input your email!" }]}
            >
              <Input
                className="email"
                placeholder="Email"
                classNames="emailinp"
              />
            </Form.Item>
            <Form.Item
              label="Varification code"
              name="code"
              rules={[
                { required: true, message: "Please input varification code!" },
              ]}
            >
              <Input className="code" placeholder="Code" />
            </Form.Item>

            <Button
              type="dashed"
              color="cyan"
              variant="filled"
              id="send"
              disabled={codeable}
              onClick={() => {
                handleSendCode();
              }}
            >
              {codeable ? `${time}s` : "Send code"}
            </Button>

            <Form.Item
              label="Password"
              name="regpassword"
              className="regpass"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password className="regpassword" placeholder="Password" />
            </Form.Item>

            <Form.Item name="remember" valuePropName="checked" label={null}>
              <Checkbox>Remember me</Checkbox>
            </Form.Item>

            <Form.Item label={null}>
              <Button type="primary" htmlType="submit">
                Register
              </Button>
            </Form.Item>
          </Form>
        )}
      </div>
    </div>
  );
}

export default Login;
