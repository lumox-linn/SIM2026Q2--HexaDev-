import "./ManageCategory.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  apiGetAllCategories,
  apiCreateCategories,
  apiEditCategories,
  apiDeleteCategories,
} from "../../../api";
import "../profileManage/profileManage.css";
import { Button, Form, Input, message, Modal, Tag, Descriptions } from "antd";

function ManageCategory() {
  const location = useLocation();
  const [categoryData, setcategoryData] = useState([]);
  const [inpWarningVisi, setinpWarningVisi] = useState(false);
  const [inpValue, setinpvalue]             = useState("");
  const [creaVisi, setcreaVisi]             = useState(false);
  const [buttype, setbuttype]               = useState("");
  const { TextArea } = Input;
  const [form] = Form.useForm();

  // ── Delete modal ──────────────────────────────────────────
  const [isModalOpen, setIsModalOpen]       = useState(false);
  const [selectedCategory, setSelectedCategory] = useState(null);

  // ── View modal ────────────────────────────────────────────
  const [viewCategory, setViewCategory]     = useState(null);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);

  const [editValue, setEditValue] = useState(null);

  // ── View handler ──────────────────────────────────────────
  const viewPro = (item) => {
    setViewCategory(item);
    setIsViewModalOpen(true);
  };

  // ── Delete handlers ───────────────────────────────────────
  const showModal = (item) => {
    setSelectedCategory(item);
    setIsModalOpen(true);
  };

  const handleOk = () => {
    setIsModalOpen(false);
    if (!selectedCategory) return;
    apiDeleteCategories(selectedCategory.id)
      .then((res) => {
        if (res.status === "success") {
          message.success(res.message);
          refresh();
        } else {
          message.error(res.error || "Failed to delete");
        }
      })
      .catch((err) => message.error(err.response?.data?.error));
  };

  const handleCancel = () => setIsModalOpen(false);

  // ── Refresh ───────────────────────────────────────────────
  const refresh = () => {
    apiGetAllCategories()
      .then((res) => {
        if (res.categories) {
          setcategoryData(
            res.categories.map((item) => ({
              id:          item.category_id,
              name:        item.category_name,
              description: item.description,
              status:      item.status,
            }))
          );
        }
      })
      .catch((err) => console.log(err.response));
  };

  useEffect(() => { refresh(); }, []);

  // ── Search ────────────────────────────────────────────────
  const searchCategory = (e) => {
    setinpvalue(e.target.value);
    if (e.target.value !== "") setinpWarningVisi(false);
    else refresh();
  };

  const searchPro = () => {
    if (inpValue !== "") {
      apiGetAllCategories({ query: inpValue })
        .then((res) => {
          if (res.categories) {
            setcategoryData(
              res.categories.map((item) => ({
                id:          item.category_id,
                name:        item.category_name,
                description: item.description,
                status:      item.status,
              }))
            );
          }
        })
        .catch((err) => {
          setcategoryData([]);
          message.error(err.response?.data?.error);
        });
    } else {
      setinpWarningVisi(true);
    }
  };

  // ── Create / Edit ─────────────────────────────────────────
  const onFinish = (values) => {
    if (buttype === "create") {
      apiCreateCategories({
        category_name: values.name,
        description:   values.description,
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
        .catch((err) => message.error(err.response?.data?.error));

    } else if (buttype === "edit") {
      apiEditCategories(Number(editValue.id), {
        category_name: values.name,        // ✅ was values.role — fixed
        description:   values.description,
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
        .catch((err) => message.error(err.response?.data?.error));
    }
  };

  const editPro = (item) => {
    document.querySelector(".pmhead")?.scrollIntoView({ behavior: "smooth" });
    setbuttype("edit");
    setEditValue(item);
    setcreaVisi(true);
    form.setFieldsValue({ name: item.name, description: item.description });
  };

  return (
    <div className="mc">
      <div className="pmhead">
        <span className="title">Category Management</span>
        <li className="sear">
          <input
            type="text"
            placeholder="Search category..."
            onChange={searchCategory}
          />
          <button onClick={searchPro}>Search</button>
          {inpWarningVisi && (
            <span className="inpWarning">Please enter a name to search</span>
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
        {/* Create / Edit form */}
        <div className={`createPro ${creaVisi ? "show" : ""}`}>
          <i onClick={() => setcreaVisi(false)}>X</i>
          <div className="createCard">
            <li>{buttype === "create" ? "Create Category" : "Edit Category"}</li>
            <Form
              name="basic"
              labelCol={{ span: 8 }}
              wrapperCol={{ span: 18 }}
              style={{ maxWidth: 600 }}
              onFinish={onFinish}
              autoComplete="off"
              form={form}
            >
              <Form.Item
                label="Category Title" name="name"
                rules={[{ required: true, message: "Please input category title!" }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Description" name="description"
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

        {/* Category cards — NO modals inside here */}
        {categoryData.map((item) => (
          <div key={item.id} className="card">
            <li className="first">
              <span className="name">{item.name}</span>
            </li>
            <span>{item.description}</span>
            <li>
              <button onClick={() => viewPro(item)}>View</button>
              <button onClick={() => editPro(item)}>Edit</button>
              <button onClick={() => showModal(item)}>Delete</button>
            </li>
          </div>
        ))}

        {/* ✅ Delete modal — outside the map */}
        <Modal
          title="Delete Confirmation"
          open={isModalOpen}
          onOk={handleOk}
          onCancel={handleCancel}
          okText="Delete"
          okType="danger"
        >
          <p>
            Are you sure you want to delete the category
            <b> {selectedCategory?.name}</b>?
          </p>
        </Modal>

        {/* ✅ View modal — outside the map */}
        <Modal
          title="Category Details"
          open={isViewModalOpen}
          onCancel={() => setIsViewModalOpen(false)}
          footer={[
            <Button key="close" onClick={() => setIsViewModalOpen(false)}>
              Close
            </Button>,
          ]}
        >
          {viewCategory && (
            <Descriptions bordered column={1} size="small">
              <Descriptions.Item label="Category ID">
                {viewCategory.id}
              </Descriptions.Item>
              <Descriptions.Item label="Category Name">
                {viewCategory.name}
              </Descriptions.Item>
              <Descriptions.Item label="Status">
                <Tag color={viewCategory.status === "active" ? "green" : "red"}>
                  {viewCategory.status?.toUpperCase()}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Description">
                {viewCategory.description || "—"}
              </Descriptions.Item>
            </Descriptions>
          )}
        </Modal>

      </div>
    </div>
  );
}

export default ManageCategory;