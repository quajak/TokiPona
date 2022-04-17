import axios from "axios";

const authService = axios.create({
    baseURL: "/api/auth",
    withCredentials: true,
    xsrfCookieName: "csrf_access_token"
});

export {authService};