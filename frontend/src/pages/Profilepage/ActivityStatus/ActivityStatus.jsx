import "./ActivityStatus.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  apiGetAllActivities,
  apiCreateActivities,
  apiEditActivities,
  apiDeleteActivities,
} from "../../../api";
import { Button, Checkbox, Form, Input, message, Modal } from "antd";
function ActivityStatus() {
  const location = useLocation();
  const [categoryData, setcategoryData] = useState([]);
  const userdata = location.state?.userdata || {};
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [inpValue, setinpvalue] = useState("");
  const [creaVisi, setcreaVisi] = useState(false);
  const [buttype, setbuttype] = useState("");
  const { TextArea } = Input;
  const [form] = Form.useForm();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [editValue, setEditValue] = useState(null);

  const showModal = (profile) => {
    setSelectedCategory(profile);
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
    if (!selectedCategory) return;
    console.log("delete");
    // try {
    //   apiDeleteActivities(selectedCategory.id)
    //     .then((res) => {
    //       console.log(res);
    //       // if (res.status === "success") {
    //       //   message.success(res.message);
    //       //   refresh();
    //       // } else {
    //       //   message.error(res.error || "Failed to delete");
    //       // }
    //     })
    //     .catch((err) => {
    //       console.log(err.response);
    //       message.error(error.response?.data?.error);
    //     });
    // } catch (error) {
    //   console.log(error);
    //   message.error(error.response?.data?.error);
    // }
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const refresh = () => {
    const userId = localStorage.getItem("userData")
      ? JSON.parse(localStorage.getItem("userData")).userid
      : null;
    console.log(userId);
    try {
      apiGetAllActivities({ user_id: userId })
        .then((res) => {
          console.log(res);
          // if (res.activities) {
          //   const activities = res.activities.map((item) => ({
          //     id: item.activity_id,
          //     name: item.activity_name,
          //     description: item.description,
          //     status: item.status,
          //   }));
          //   setcategoryData(activities);
          // }
        })
        .catch((err) => {
          console.log(err.response);
          // message.error(err.response?.data?.error);
        });
    } catch (error) {
      console.log(error);
      // message.error(error.response?.data?.error);
    }
  };

  const searchCategory = (e) => {
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
        apiGetAllActivities({ query: inpValue })
          .then((res) => {
            console.log(res);
            // if (res.activities) {
            //   const activities = res.activities.map((item) => ({
            //     id: item.activity_id,
            //     name: item.activity_name,
            //     description: item.description,
            //     status: item.status,
            //   }));
            //   setcategoryData(activities);
            // }
          })
          .catch((err) => {
            setcategoryData([]);
            message.error(err.response?.data?.error);
          });
      } catch (error) {
        message.error(error.response?.data?.error);
      }
    } else {
      // if the input value is empty
      setinpWarningVisi(true);
    }
  };

  // const getStatusClass = (item) => {
  //   if (item.status === "suspended") return "disabled";
  //   return "active";
  // };

  const onFinish = (values) => {
    try {
      if (buttype === "create") {
        console.log("create");
        // apiCreateActivities({
        //   activity_name: values.name,
        //   description: values.description,
        // })
        //   .then((res) => {
        //     console.log(res);
        //     // if (res.status === "success") {
        //     //   message.success(res.message);
        //     //   setcreaVisi(false);
        //     //   form.resetFields();
        //     //   refresh();
        //     // } else {
        //     //   message.error(res.error || res.message);
        //     // }
        //   })
        //   .catch((err) => message.error(err.response?.data?.error));
      } else if (buttype === "edit") {
        console.log("edit");
        // apiEditActivities(Number(editValue.id), {
        //   activity_name: values.role,
        //   description: values.description,
        // })
        //   .then((res) => {
        //     console.log(res);
        //     // if (res.status === "success") {
        //     //   message.success(res.message);
        //     //   setcreaVisi(false);
        //     //   form.resetFields();
        //     //   refresh();
        //     // } else {
        //     //   message.error(res.error || res.message);
        //     // }
        //   })
        //   .catch((err) => {
        //     message.error(err.response?.data?.error);
        //   });
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
    setEditValue(item);
    setcreaVisi(true);
    form.setFieldsValue({
      name: item.name,
      description: item.description,
    });
  };
  return (
    <div className="mc">
      <div className="pmhead">
        <span className="title">Category management</span>
        <li>
          <input
            type="text"
            placeholder="Search category..."
            onChange={(e) => searchCategory(e)}
          />
          <button onClick={searchPro}>Search</button>
          {inpWarningVisi ? (
            <span className="inpWarning">Please enter a name to search</span>
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
            + Create New Category
          </button>
        </li>
      </div>

      <div className="profileContent">
        <div className={`createPro ${creaVisi ? "show" : ""}`}>
          <i onClick={() => setcreaVisi(false)}>X</i>
          <div className="createCard">
            <li>
              {buttype === "create"
                ? "Create Category"
                : buttype === "edit"
                  ? "Edit Category"
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
                label="Category Title"
                name="name"
                rules={[
                  { required: true, message: "Please input category title!" },
                ]}
              >
                <Input />
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
        <div className="card">
          <li className="first">category</li>
          <span>description</span>

          <li>
            <button onClick={() => editPro("0")}>Edit</button>
            <button onClick={() => showModal("1")}>Delete</button>
            <Modal
              title="Suspension Confirmation"
              open={isModalOpen}
              onOk={handleOk}
              onCancel={handleCancel}
              okText="Delete"
              okType="danger"
            >
              <p>
                Are you sure you want to delete this
                {/* <b>{selectedCategory?.role}</b>? */}
              </p>
            </Modal>
          </li>
        </div>
        {/* {categoryData.map((item) => {
          return (
            <div key={item.id} className="card">
              <li className="first">
                {/* <div className="img">
                  {item.role === "admin"
                    ? "UA"
                    : item.role === "platform_manager"
                      ? "PM"
                      : item.role === "fund_raiser"
                        ? "FR"
                        : item.role === "donee"
                          ? "DO"
                          : item.role.substring(0, 2).toUpperCase()}
                </div> */}
        {/* <span className="name">{item.name}</span> */}

        {/* <div className={getStatusClass(item)}>
                  {item.status === "active" ? "Active" : "Suspended"}
                </div>*/}
        {/* </li>
              <span>{item.description}</span>

              <li>
                <button onClick={() => editPro(item)}>Edit</button>
                <button onClick={() => showModal(item)}>Delete</button> */}

        {/* {item.status === "active" ? (
                  <button onClick={() => showModal(item)}>Suspend</button>
                ) : (
                  <button
                    onClick={() => handleActivate(item)}
                    className="activeBut"
                  >
                    Activate
                  </button>
                )} */}
        {/* <Modal
                  title="Suspension Confirmation"
                  open={isModalOpen}
                  onOk={handleOk}
                  onCancel={handleCancel}
                  okText="Delete"
                  okType="danger"
                >
                  <p>
                    Are you sure you want to delete the category
                    <b> {selectedCategory?.name}?</b>
                  </p>
                </Modal>
              </li>
            </div> */}
        {/* ); */}
        {/* })} */}
      </div>
    </div>
  );
}
export default ActivityStatus;
