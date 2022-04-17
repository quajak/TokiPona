import "./assets/bulma.scss"
import "@fortawesome/fontawesome-free/scss/fontawesome.scss"
import "@fortawesome/fontawesome-free/scss/regular.scss"
import "@fortawesome/fontawesome-free/scss/solid.scss"

import { createApp } from 'vue'
import App from './App.vue'
import HelloWorld from "./components/HelloWorld.vue"
import { createRouter, createWebHashHistory, RouterView } from 'vue-router'
import Login from "./components/Login.vue"
import store, { ActionTypes } from './store/store'
import Register from "./components/Register.vue"
import axios from 'axios'
import Logout from "./components/Logout.vue"
import Oruga from '@oruga-ui/oruga-next'
import '@oruga-ui/oruga-next/dist/oruga.css'
import { bulmaConfig } from "@oruga-ui/theme-bulma"
import Flashcard from "./components/Flashcard.vue"


axios.defaults.xsrfCookieName = "csrf_access_token"
axios.defaults.xsrfHeaderName = "X-CSRF-TOKEN"

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
  {path: "/", component: HelloWorld},
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/logout', component: Logout },
  { path: "/flashcard", component: Flashcard}
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

// get start up data

store.dispatch(ActionTypes.fetchUser)