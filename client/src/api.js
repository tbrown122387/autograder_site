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
  async requestPasswordReset(email) {
    const body = { email: email };
    return axios.post(`${apiUrl}${apiV1}/auth/request_password_reset`, body);
  },
  async resetPasswordToken(email, password, token) {
    let formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    formData.append("pw_reset_token", token);
    return axios.post(`${apiUrl}${apiV1}/auth/reset_password_from_token`, formData);
  },

  async getAssignments(token) {
    return axios.get(`${apiUrl}${apiV1}/assignments`, getAuthHeaders(token));
  },
  async getAssignment(token, assignmentId) {
    return axios.get(`${apiUrl}${apiV1}/assignment/${assignmentId}`, getAuthHeaders(token));
  },
  async saveAssignment(token, assignmentId, bundleName, assignmentName, testsCollections, packageNames, datasets, setupCode) {
    const body = {};
    if (assignmentId) body["assignment_id"] = assignmentId;
    if (bundleName) body["bundle_name"] = bundleName;
    if (assignmentName) body["assignment_name"] = assignmentName;
    if (testsCollections.length) body["tests_collection"] = testsCollections;
    if (packageNames) body["package_names"] = packageNames;
    if (datasets.length) body["datasets"] = datasets;
    if (setupCode) body["setup_code"] = setupCode;

    return axios.post(`${apiUrl}${apiV1}/save_assignment`, body, getAuthHeaders(token));
  },
  async createAssignment(token) {
    const body = {
      // default value
      tests_collection: [{ label: "", visibility: "", code: "" }],
      datasets: [],
    };
    return axios.post(`${apiUrl}${apiV1}/save_assignment`, body, getAuthHeaders(token));
  },
  async deleteAssignment(token, assignmentId) {
    const body = { assignment_id: assignmentId };
    return axios.post(`${apiUrl}${apiV1}/delete_assignment`, body, getAuthHeaders(token));
  },
  async downloadBundle(assignmentName, datasets, packages, testsCollection) {
    let formData = new FormData();

    // TODO: change backend to accept testsCollection JSON instead of arrays
    const labels = testsCollection.map((test) => test.label);
    const visibilities = testsCollection.map((test) => test.visibility);
    const codes = testsCollection.map((test) => test.code);

    formData.append("assignment_name", assignmentName);
    formData.append("labels", JSON.stringify(labels));
    formData.append("visibilities", JSON.stringify(visibilities));
    formData.append("codes", JSON.stringify(codes));

    if (datasets) {
      for (let file of datasets) {
        formData.append("datasets", file, file.name);
      }
    }

    if (packages) {
      formData.append("package_names", JSON.stringify(packages.split(",")));
    }

    return axios.post(`${apiUrl}${apiV1}/uploadfile`, formData, {
      responseType: "blob",
    });
  },
};
