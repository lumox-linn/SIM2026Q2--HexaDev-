import { Route, Routes } from "react-router-dom";
import React from "react";
import Router from "./Router";
function RouterView() {
  console.log(Router);
  return (
    <Routes>
      <Route path="/test" element={<h1>The routing is working</h1>} />
      {Router.map((item, index) => (
        <Route
          key={index}
          path={item.path}
          element={React.cloneElement(item.element, { Router })}
        >
          {item.children &&
            item.children.map((child, childIndex) => (
              <Route
                key={childIndex}
                path={child.path}
                element={child.element}
              />
            ))}
        </Route>
      ))}
    </Routes>
  );
}
export default RouterView;
