import "./ManageCategory.css";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import {
  apiGetAllCategories,
  apiCreateCategories,
  apiEditCategories,
  apiDeleteCategories,
} from "../../../api";
// import "../profileManage/profileManage.css";
// import { Button, Checkbox, Form, Input, message, Modal } from "antd";
function ManageCategory() {
  const refresh = () => {
    try {
      apiGetAllCategories()
        .then((res) => {
          console.log(res);
          // if (res.categories) {
          //   const categories = res.categories.map((item) => ({}));
          //   setprofileData(categories);
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

  useEffect(() => {
    refresh();
  }, []);
  return <div>111</div>;
}
export default ManageCategory;
