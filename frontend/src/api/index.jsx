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
  console.log(params);
  return newRequest({ url: "/api/accounts/", method: "get", params });
}

export function apiGetAccount(id) {
  return newRequest({ url: `/api/accounts/${id}`, method: "get" });
}

export function apiCreateAcc(data) {
  console.log(data);
  return newRequest({ url: "/api/auth/accounts", method: "post", data: data });
}

export function apiUpdateAcc(id, data) {
  console.log(data);
  return newRequest({ url: `/api/accounts/${id}`, method: "put", data: data });
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

// ── Profile Management ───────────────────────────────────────

export function apiGetAllProfiles(params) {
  return newRequest({ url: "/api/profiles/", method: "get", params: params });
}

export function apiCreateProfile(data) {
  return newRequest({ url: "/api/profiles/", method: "post", data: data });
}

export function apiEditProfile(id, data) {
  console.log(id, data);
  return newRequest({ url: `/api/profiles/${id}`, method: "put", data: data });
}

export function apiSuspendProfile(id) {
  return newRequest({ url: `/api/profiles/${id}/suspend`, method: "put" });
}

export function apiActivateProfile(id) {
  return newRequest({ url: `/api/profiles/${id}/activate`, method: "put" });
}

// categories
export function apiGetAllCategories(params) {
  console.log(params);
  return newRequest({ url: "/api/categories/", method: "get", params: params });
}

export function apiCreateCategories(data) {
  return newRequest({ url: "/api/categories/", method: "post", data: data });
}

export function apiEditCategories(id, data) {
  console.log(id, data);
  return newRequest({
    url: `/api/categories/${id}`,
    method: "put",
    data: data,
  });
}

export function apiDeleteCategories(id) {
  console.log("delete", id);
  return newRequest({ url: `/api/categories/${id}`, method: "delete" });
}

// activities
export function apiGetAllActivities(params) {
  console.log(params);
  return newRequest({ url: "/api/activities/", method: "get", params: params });
}

export function apiCreateActivities(data) {
  return newRequest({ url: "/api/activities/", method: "post", data: data });
}

export function apiEditActivities(id, data) {
  console.log(id, data);
  return newRequest({
    url: `/api/activities/${id}`,
    method: "put",
    data: data,
  });
}

export function apiDeleteActivities(id) {
  console.log("delete", id);
  return newRequest({ url: `/api/activities/${id}`, method: "delete" });
}
// donee
// Donation history
export function apiMyDonations(params = {}) {
  return newRequest({
    url: "/api/history/donee",
    method: "get",
    params: params,
  });
}

// Browse activities
export function apiGetDoneeActivities(params = {}) {
  return newRequest({
    url: "/api/donee/activities",
    method: "get",
    params,
  });
}

// Get favourites
export function apiGetAllFavorites() {
  return newRequest({ url: "/api/donee/favourites", method: "get" });
}

// Save favourite
export function apiSaveFavourite(activity_id) {
  return newRequest({
    url: "/api/donee/favourites",
    method: "post",
    data: { activity_id: activity_id },
  });
}

// Remove favourite
export function apiRemoveFavorites(activity_id) {
  return newRequest({
    url: `/api/donee/favourites/${activity_id}`,
    method: "delete",
  });
}

export function apiMyDonations(params, token) {
  console.log(params, token);
  return newRequest({
    url: "/api/history/donee",
    method: "get",
    params: params,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}
// // favorites
// export function apiGetAllFavorites(params, token) {
//   return newRequest({
//     url: "/api/donee/favourites",
//     method: "get",
//     data: params,
//     headers: {
//       Authorization: `Bearer ${token}`,
//     },
//   });
// }
// export function apiRemoveFavorites(userid, data) {
//   return newRequest({
//     url: `/api/remove/${userid}`,
//     method: "put",
//     data: data,
//   });
// }
