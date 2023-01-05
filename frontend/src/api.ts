import axios from "axios";
axios.defaults.xsrfCookieName = "csrf_access_token"
axios.defaults.xsrfHeaderName = "X-CSRF-TOKEN"

export const basePath = localStorage.getItem("basePath") || "https://kama-sona-server.justso.de"

const authService = axios.create({
    baseURL: basePath + "/api/auth",
    withCredentials: true,
    xsrfCookieName: "csrf_access_token"
});

export {authService};
