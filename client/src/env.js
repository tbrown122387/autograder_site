const envApiUrl = process.env.NODE_ENV === "production" ? "https://autograder-site.herokuapp.com" : "http://localhost:5001";
const API_V1 = "/api/v1";

export const apiUrl = envApiUrl;
export const apiV1 = API_V1;
