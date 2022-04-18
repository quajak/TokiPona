import axios from "axios";

axios.defaults.xsrfCookieName = "csrf_access_token"
axios.defaults.xsrfHeaderName = "X-CSRF-TOKEN"

const authService = axios.create({
    baseURL: "/api/auth",
    withCredentials: true,
    xsrfCookieName: "csrf_access_token"
});

export {authService};