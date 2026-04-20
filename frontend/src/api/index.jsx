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
  // console.log(data);
  return newRequest({
    url: "/logout/",
    method: "post",
    data: data,
  });
}
export function apiUserinfo(data) {
  // console.log(data);
  return newRequest({
    url: "/userInfo/",
    method: "post",
    data: data,
  });
}
export function apiCreateAcc(data) {
  console.log(data);
  return newRequest({
    url: "/createAcc/",
    method: "post",
    data: data,
  });
}
export function apiUpdateAcc(data) {
  console.log(data);
  return newRequest({
    url: "/updateAcc/",
    method: "post",
    data: data,
  });
}

export function apiProfileinfo(data) {
  return newRequest({
    url: "/profileinfo/",
    method: "post",
    data: data,
  });
}

export function apiCreateProfile(data) {
  return newRequest({
    url: "/createProfile/",
    method: "post",
    data: data,
  });
}

export function apiEditProfile(data) {
  return newRequest({
    url: "/editProfile/",
    method: "post",
    data: data,
  });
}
export function apiSuspendProfile(data) {
  return newRequest({
    url: "/suspendProfile/",
    method: "post",
    data: data,
  });
}
