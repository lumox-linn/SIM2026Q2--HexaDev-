import axios from "axios";
import cookie from "js-cookie";

const request = axios.create({
  baseURL: "https://sim2026q2-hexadev-production-5c1d.up.railway.app",
  // baseURL: "http://127.0.0.1:5000",
  timeout: 20000,
  timeoutErrorMessage: "request timeout",
});
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token") || cookie.get("token");
    if (token) {
      config.headers.authorization = `Bearer ${token}`;
    }
    return config;
  },
  (err) => {
    return Promise.reject(err);
  },
);
request.interceptors.response.use(
  (config) => {
    console.log(
      "!!! The interceptor got the original response from the backend:",
      // config.data,
    );
    return config.data;
  },
  (err) => {
    // if (err.response && err.response.status === 401) {
    //   console.warn("Login expired, redirecting to home page...");
    //   localStorage.removeItem("token");
    //   localStorage.removeItem("userData");
    //   cookie.remove("token");
    //   window.location.href = "/home";
    // }
    console.error("!!! the interceptor caught a network error:", err);
    const msg = err.response?.data?.msg || "server error";
    return Promise.reject(err);
  },
);
function newRequest(config) {
  const { url, method = "get", data = {}, params = {} } = config;
  return request({
    url,
    method,
    data,
    params,
  });
}
export default newRequest;
