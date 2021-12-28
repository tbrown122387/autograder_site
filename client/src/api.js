import axios from "axios";
import { apiUrl, apiV1 } from "./env";

function getAuthHeaders(token) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(email, password) {
    let formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);
    return axios.post(`${apiUrl}${apiV1}/auth/token`, formData);
  },
  async registerAccount(email, password) {
    let formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    formData.append("full_name", "full_name");
    formData.append("username", "username");
    return axios.post(`${apiUrl}${apiV1}/auth/register`, formData);
  },
  async getAccount(token) {
    return axios.get(`${apiUrl}${apiV1}/auth/account`, getAuthHeaders(token));
  },
};
