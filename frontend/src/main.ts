import { createApp } from 'vue'
import App from './App.vue'
import HelloWorld from "./components/HelloWorld.vue"
import { createRouter, createWebHashHistory, RouterView } from 'vue-router'
import Login from "./components/Login.vue"
import store, { ActionTypes } from './store/store'
import Register from "./components/Register.vue"
import axios from 'axios'
import Logout from "./components/Logout.vue"

axios.defaults.xsrfCookieName = "CSRF-TOKEN"
axios.defaults.xsrfHeaderName = "X-CSRF-TOKEN"

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  {path: "/", component: HelloWorld},
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/logout', component: Logout },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
})
const app = createApp(App)
app.use(store)
app.use(router)

app.mount('#app')

// get start up data

store.dispatch(ActionTypes.fetchUser)