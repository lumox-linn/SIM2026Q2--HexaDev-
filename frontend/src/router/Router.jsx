import { Children, lazy } from "react";
import { Navigate } from "react-router-dom";
const Home = lazy(() => import("../pages/Home/Home"));
const Login = lazy(() => import("../pages/Login/Login"));
const Profile = lazy(() => import("../pages/profile/Profile"));
const Donate = lazy(() => import("../pages/navigationbar/Donate/Donate"));
const About = lazy(() => import("../pages/about/About"));
const Activities = lazy(() => import("../pages/Activities/activities"));
const Personalinfo = lazy(
  () => import("../pages/Profilepage/personalinfo/personalinfo"),
);
const Fundraise = lazy(
  () => import("../pages/navigationbar/Fondraise/Fundraise"),
);
const MyActivities = lazy(
  () => import("../pages/Profilepage/myActivities/myactivities"),
);
const ManageAccount = lazy(
  () => import("../pages/Profilepage/mangeAccount/ManageAccount"),
);
const ManageCategory = lazy(
  () => import("../pages/Profilepage/ManageCategories/manageCategory"),
);

const ManageActivities = lazy(
  () => import("../pages/Profilepage/ManageActivities/ManageActivities"),
);

const ActivityStatus = lazy(
  () => import("../pages/Profilepage/ActivityStatus/ActivityStatus"),
);
const DefaultPage = lazy(
  () => import("../pages/Profilepage/proDefaultpage/DefaultPage"),
);
const ManageProfile = lazy(
  () => import("../pages/Profilepage/profileManage/profileManage"),
);

const Router = [
  {
    path: "/",
    element: <Navigate to="/home" />,
  },
  {
    path: "/home",
    stuff: {},
    element: <Home />,
  },
  {
    path: "/login",
    stuff: { title: "Login" },
    element: <Login />,
  },
  {
    path: "/profile/:id/*",
    stuff: { title: "User profile" },
    element: <Profile />,
    children: [
      {
        index: true,
        stuff: {},
        element: <DefaultPage />,
      },

      {
        path: "personalinfo",
        stuff: { title: "UserPersonal Info" },
        element: <Personalinfo />,
      },
      {
        path: "ManageProfile",
        stuff: { title: "Profile management" },
        element: <ManageProfile />,
      },
      {
        path: "myactivities",
        stuff: { title: "My Activities" },
        element: <MyActivities />,
      },
      {
        path: "ManageAccount",
        stuff: { title: "User Management" },
        element: <ManageAccount />,
      },
      {
        path: "ManageCategory",
        stuff: { title: "Manage Category" },
        element: <ManageCategory />,
      },
      {
        path: "ManageActivities",
        stuff: { title: "Activity Management" },
        element: <ManageActivities />,
      },
      {
        path: "ActivityStatus",
        stuff: { title: "Activity Status" },
        element: <ActivityStatus />,
      },
    ],
  },
  {
    path: "/donate",
    nav: { title: "Donate" },
    element: <Donate />,
  },
  {
    path: "/fundraise",
    nav: { title: "Fundraise" },
    element: <Fundraise />,
  },
  {
    path: "/about",
    stuff: { title: "About" },
    element: <About />,
  },
  {
    path: "/activities",
    stuff: { title: "Activities" },
    element: <Activities />,
  },
];
export default Router;
