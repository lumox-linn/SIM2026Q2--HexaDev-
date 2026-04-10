import newRequest from "../utils/request";

export function apiLogin(data) {
  return newRequest({
    url: "/auth/login",
    method: "post",
    data: data,
  });
}
export function apiRegister(data) {
  return newRequest({
    url: "/auth/register",
    method: "post",
    data: data,
  });
}
export function apiLogout(data) {
  return newRequest({
    url: "/auth/logout",
    method: "post",
    data: data,
  });
}
export function apiGetMe() {
  return newRequest({
    url: "/auth/me",
    method: "get",
  });
}
export function apiGetAccounts() {
  return newRequest({
    url: "/auth/accounts",
    method: "get",
  });
}
export function apiCreateAcc(data) {
  return newRequest({
    url: "/auth/accounts",
    method: "post",
    data: data,
  });
}
