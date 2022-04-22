import "./assets/bulma.scss"
import "@fortawesome/fontawesome-free/scss/fontawesome.scss"
import "@fortawesome/fontawesome-free/scss/regular.scss"
import "@fortawesome/fontawesome-free/scss/solid.scss"

import { createApp } from 'vue'
import App from './App.vue'
import HelloWorld from "./components/HelloWorld.vue"
import { createRouter, createWebHashHistory, RouterView } from 'vue-router'
import Login from "./components/Login.vue"
import store, { ActionTypes, MutationTypes } from './store/store'
import Register from "./components/Register.vue"
import axios from 'axios'
import Logout from "./components/Logout.vue"
import Oruga from '@oruga-ui/oruga-next'
import '@oruga-ui/oruga-next/dist/oruga.css'
import { bulmaConfig } from "@oruga-ui/theme-bulma"
import Flashcard from "./components/Flashcard.vue"
import Profile from "./components/Profile.vue"

axios.defaults.xsrfCookieName = "csrf_access_token"
axios.defaults.xsrfHeaderName = "X-CSRF-TOKEN"

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  {path: "/", component: HelloWorld},
  { path: '/login', component: Login, props: {redirectReason: ""} },
  { path: '/relogin', component: Login, props: true },
  { path: '/register', component: Register },
  { path: "/flashcard", component: Flashcard},
  { path: "/profile", component: Profile}
]

const router = createRouter({
  history: createWebHashHistory(),
  routes, // short for `routes: routes`
})
const app = createApp(App)
app.use(store)
app.use(router)
app.use(Oruga, {
    customIconPacks: {
      fas: {
        sizes: {
          default: "",
          small: "fa-sm",
          medium: "fa-lg",
          large: "fa-2x",
        },
      },
    },
    iconPack: "fas",
    ...bulmaConfig,
})

app.mount('#app')

axios.interceptors.response.use(function (response) {
    // Do something with response data
    return response;
  }, function (error) {
    if(error.response.status == 401){
      router.push({path: "/relogin", params: {redirectReason: "Due to inactivity you have to login again"}})
      store.commit(MutationTypes.logoutUserState)
    }
    // Do something with response error
    return Promise.reject(error);
  });

// get start up data

store.dispatch(ActionTypes.fetchUser)

