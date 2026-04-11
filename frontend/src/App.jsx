import RouterView from "./router/RouterView";
import Router from "./router/Router";
import "./App.css";
import React, { Suspense, useEffect, useRef } from "react";
import { BrowserRouter, useLocation } from "react-router-dom";
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
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
