<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {useStore} from "vuex";
import {ActionTypes} from "./store/store"
import { useRouter} from "vue-router"
import {computed} from "vue";

const store = useStore()

const loggedIn = computed(() => store.state.isLoggedIn)

</script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-primary bg-gradient">
      <div class="container-fluid">
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <div v-if="!loggedIn">
              <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
              </li>
              <li>
                <router-link to="/register" class="nav-link">Register</router-link>
              </li>
            </div>
            <div v-else>
              <li class="nav-item">
                <router-link to="/flashcard" class="nav-link">Practise</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/logout" class="nav-link">Logout</router-link>
              </li>
            </div>
          </ul>
        </div>
      </div>
    </nav>
  </div>
  <router-view></router-view>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
