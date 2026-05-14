import RouterView from "./router/RouterView";
import Router from "./router/Router";
import "./App.css";
import React, { Suspense, useEffect, useRef } from "react";
import chicken from "./assets/chicken.svg";
import { useState } from "react";
import { BrowserRouter, useLocation } from "react-router-dom";
// import { apiGetAllCategories } from "../../../api";
function AppContent() {
  return (
    <div className="App">
      <Suspense fallback={<div>Loading....</div>}>
        <RouterView allRouter={Router} />
      </Suspense>
    </div>
  );
}

function App() {
  // useEffect(() => {
  //   try {
  //     apiGetAllCategories()
  //       .then((res) => {
  //         console.log(res);
  //         // if (res.categories) {
  //         //   const categories = res.categories.map((item) => ({
  //         //     id: item.category_id,
  //         //     name: item.category_name,
  //         //     description: item.description,
  //         //     status: item.status,
  //         //   }));
  //         //   setcategoryData(categories);
  //         // }
  //       })
  //       .catch((err) => {
  //         console.log(err.response);
  //         // message.error(err.response?.data?.error);
  //       });
  //   } catch (error) {
  //     console.log(error);
  //     // message.error(error.response?.data?.error);
  //   }
  // });
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
