import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Checkbox, Form, Input, message, Select } from "antd";
import { ArrowLeftOutlined } from "@ant-design/icons";
import "../Login/login.css";
import { apiLogin, apiRegister, apiSendCode } from "../../api";
import cookie from "js-cookie";

function Login() {
  const [form] = Form.useForm();
  const [register, setregister] = useState(false);
  const [show, setshow] = useState(false);
  const [codeable, setcodeable] = useState(false);
  const [time, settime] = useState(30);
  const [loginstatus, setloginstatus] = useState(false);
  const navigate = useNavigate();
  // const handleSendCode = async () => {
  //   try {
  //     // get value from the form
  //     const email = form.getFieldValue("email");

  //     if (
  //       !email ||
  //       !/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(email)
  //     ) {
  //       alert("Please enter a valid email address!");
  //       return;
  //     } else {
  //       setcodeable(true);
  //     }

  //     //call api
  //     const res = await apiSendCode({ email });

  //     if (res.status === "success") {
  //       console.log("Varification code sent:", email);
  //     } else {
  //       alert(res.message || "Send failed");
  //     }
  //   } catch (err) {
  //     console.error("network:", err);
  //   }
  // };
  const onFinish = async (values) => {
    try {
      const res = await apiLogin(values);
      if (res.status == "success") {
        localStorage.setItem("token", res.token);
        localStorage.setItem(
          "userData",
          JSON.stringify({
            role: res.role,
            // role_label: res.role_label,
            userid: res.user_id,
            username: res.username,
            useravatar: res.avatar_url,
            email: res.email,
            loginstatus: res.loginstatus,
            phone: res.phone,
            dob: res.dob,
            activity: res.avtivity,
          }),
        );

        window.dispatchEvent(new Event("storage"));
        message.open({
          type: "success",
          content: "Login success",
        });
        setTimeout(() => {
          navigate(res.redirectTo, {
            state: {
              userdata: localStorage.getItem("userData"),
              fromLogin: true,
            },
          });
        }, 1000);
      } else if (res.status === "fail") {
        console.log(res);
        if (res.reason) {
          message.open({
            type: "error",
            content: "Wrong identity",
          });
        } else {
          setshow(true);
        }

        return Promise.reject(new Error(res.message || "Login failed"));
      }
      form.resetFields();
    } catch (err) {
      console.log(err.response);
      message.error(err.response?.data?.error);
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
  const onValuesChange = (_, v) => {
    // when input is empty set alart message to false
    if (v.username === "" || v.password === "") {
      setshow(false);
    }
  };
  const handleChange = (value) => {
    console.log(`selected ${value}`);
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
  };
  return (
    <div className="login">
      <div className="loginbox">
        <ArrowLeftOutlined
          onClick={() => {
            navigate("/home");
          }}
        />

        <span className="companyname">HopeLink</span>

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
          onValuesChange={onValuesChange}
        >
          <Form.Item
            label="Username"
            name="username"
            rules={[{ required: true, message: "Please input your username!" }]}
          >
            <Input className="username" placeholder="username" />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: "Please input your password!" }]}
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
                { label: <span>Admin</span>, value: "Admin" },

                {
                  label: <span>Platform Manager</span>,
                  value: "Platform Manager",
                },
                {
                  label: <span>Donee</span>,
                  value: "Donee",
                },
                {
                  label: <span>Fund Raiser</span>,
                  value: "Fund Raiser",
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
        </Form>
      </div>
    </div>
  );
}

export default Login;
