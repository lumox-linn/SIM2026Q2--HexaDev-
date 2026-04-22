import newRequest from "../utils/request";


export function apiLogin(data) {
  console.log(data);
  return newRequest({
    url: "/api/auth/login",
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
    url: "/api/profiles/",
    method: "post",
    data: data,
  });
}

export function apiCreateProfile(data) {
  return newRequest({
    url: "/api/profiles/",
    method: "post",
    data: data,
  });
}

export function apiEditProfile(id, data) {
  return newRequest({
    url: `/api/profiles/${id}`,
    method: "put",
    data: data,
  });
}
export function apiSuspendProfile(id) {
  return newRequest({
    url: `/api/profiles/${id}/suspend`,
    method: "put",
  });
}
export function apiSuspendUser(data) {
  return newRequest({
    url: "/suspendUser/",
    method: "post",
    data: data,
  });
}



// Account management
export function apiGetAllAccounts(params) {
  return newRequest({ url: '/api/accounts/', method: 'get', params })
}
export function apiGetAccount(id) {
  return newRequest({ url: `/api/accounts/${id}`, method: 'get' })
}
export function apiUpdateAccount(id, data) {
  return newRequest({ url: `/api/accounts/${id}`, method: 'put', data })
}
export function apiSuspendAccount(id) {
  return newRequest({ url: `/api/accounts/${id}/suspend`, method: 'put' })
}
export function apiActivateAccount(id) {
  return newRequest({ url: `/api/accounts/${id}/activate`, method: 'put' })
}
export function apiSearchAccounts(params) {
  return newRequest({ url: '/api/accounts/', method: 'get', params })
}

// Profile management
export function apiGetAllProfiles() {
  return newRequest({ url: '/api/profiles/', method: 'get' })
}
export function apiActivateProfile(id) {
  return newRequest({ url: `/api/profiles/${id}/activate`, method: 'put' })
}