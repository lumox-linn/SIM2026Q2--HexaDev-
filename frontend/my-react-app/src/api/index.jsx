import newRequest from "../utils/request";

export function apiLogin(data) {
  console.log(data);
  return newRequest({
    url: "/login/",
    method: "post",
    data: data,
  });
}
export function apiRegister(data) {
  console.log(data);
  return newRequest({
    url: "/register/",
    method: "post",
    data: data,
  });
}
export function apiSendCode(data) {
  return newRequest({
    url: "/send_code/",
    method: "post",
    data: data,
  });
}
export function apiLogout(data) {
  console.log(data);
  return newRequest({
    url: "/logout/",
    method: "post",
    data: data,
  });
}
