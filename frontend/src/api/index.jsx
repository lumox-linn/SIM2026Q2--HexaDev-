import newRequest from "../utils/request";

// ── Auth ─────────────────────────────────────────────────────
export function apiLogin(data) {
  console.log(data);
  return newRequest({ url: "/api/auth/login", method: "post", data });
}

export function apiRegister(data) {
  return newRequest({ url: "/api/auth/register", method: "post", data });
}

export function apiSendCode(data) {
  return newRequest({ url: "/api/auth/send_code", method: "post", data });
}

export function apiLogout(data) {
  return newRequest({ url: "/api/auth/logout", method: "post", data });
}

// ── Account Management ───────────────────────────────────────
export function apiGetAllAccounts(params) {
  return newRequest({ url: "/api/accounts/", method: "get", params });
}

export function apiGetAccount(id) {
  return newRequest({ url: `/api/accounts/${id}`, method: "get" });
}

export function apiCreateAcc(data) {
  return newRequest({ url: "/api/auth/accounts", method: "post", data: data });
}

export function apiUpdateAcc(id, data) {
  return newRequest({ url: `/api/accounts/${id}`, method: "put", data });
}

export function apiSuspendAccount(id) {
  return newRequest({ url: `/api/accounts/${id}/suspend`, method: "put" });
}

export function apiActivateAccount(id) {
  return newRequest({ url: `/api/accounts/${id}/activate`, method: "put" });
}

export function apiSearchAccounts(params) {
  console.log(params);
  return newRequest({ url: "/api/accounts/", method: "get", params });
}

export function apiSuspendUser(data) {
  // kept for backward compatibility — use apiSuspendAccount(id) instead
  return newRequest({
    url: `/api/accounts/${data.user}/suspend`,
    method: "put",
  });
}

// ── Profile Management ───────────────────────────────────────
export function apiProfileinfo(params) {
  return newRequest({ url: "/api/profiles/", method: "get", params });
}

export function apiGetAllProfiles(params) {
  return newRequest({ url: "/api/profiles/", method: "get", params });
}

export function apiCreateProfile(data) {
  return newRequest({ url: "/api/profiles/", method: "post", data });
}

export function apiEditProfile(id, data) {
  return newRequest({ url: `/api/profiles/${id}`, method: "put", data });
}

export function apiSuspendProfile(id) {
  return newRequest({ url: `/api/profiles/${id}/suspend`, method: "put" });
}

export function apiActivateProfile(id) {
  return newRequest({ url: `/api/profiles/${id}/activate`, method: "put" });
}

export function apiUserinfo(params) {
  return newRequest({ url: "/api/accounts/", method: "get", params });
}
