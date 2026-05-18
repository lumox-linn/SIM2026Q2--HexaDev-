import { Children, lazy } from "react";
import { Navigate } from "react-router-dom";
const Home = lazy(() => import("../pages/Home/Home"));
const Login = lazy(() => import("../pages/Login/Login"));
const Profile = lazy(() => import("../pages/profile/Profile"));
const Donate = lazy(() => import("../pages/navigationbar/Donate/Donate"));
const About = lazy(() => import("../pages/about/About"));
const Activities = lazy(() => import("../pages/Activities/activities"));
const Report = lazy(() => import("../pages/Profilepage/personalinfo/Report"));
const Fundraise = lazy(
  () => import("../pages/navigationbar/Fondraise/Fundraise"),
);
const MyDonations = lazy(
  () => import("../pages/Profilepage/myDonations/myDonations"),
);
const ManageAccount = lazy(
  () => import("../pages/Profilepage/mangeAccount/ManageAccount"),
);
const ManageCategory = lazy(
  () => import("../pages/Profilepage/ManageCategories/manageCategory"),
);

const Favorites = lazy(() => import("../pages/Favorites/Favorites"));

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
    path: "/favorites/:id",
    stuff: { title: "User Favorites" },
    element: <Favorites />,
  },
  {
    path: "/profile/:id/*",
    stuff: { title: "User profile" },
    element: <Profile />,
    children: [
      {
        path: "Report",
        stuff: { title: "Report" },
        element: <Report />,
      },
      {
        path: "ManageProfile",
        stuff: { title: "Profile management" },
        element: <ManageProfile />,
      },
      {
        path: "myDonations",
        stuff: { title: "My Activities" },
        element: <MyDonations />,
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
