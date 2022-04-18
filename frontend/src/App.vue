<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import {useStore} from "vuex";
import {ActionTypes} from "./store/store"
import { useRouter} from "vue-router"
import {computed, ref} from "vue";

const store = useStore()

const loggedIn = computed(() => store.state.isLoggedIn)

const expanded = ref(false);

</script>

<template>
  <div>
    <nav class="navbar">
      <div class="navbar-brand">
        <h3 class="title is-3" style="margin: 0px">Kama Sona</h3>

        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" @click="expanded = !expanded" :class="expanded ? 'is-active' : ''">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>
      <div class="navbar-menu" :class="expanded ? 'is-active' : ''">
        <div class="navbar-start">
          <div class="navbar-item">
            <router-link to="/">Home</router-link>
          </div>
          <div class="navbar-item" v-if="loggedIn">
            <router-link to="/flashcard">Practise</router-link>
          </div>
        </div>
        <div class="navbar-end">
          <div class="navbar-item" v-if="!loggedIn">
            <router-link to="/login" class="nav-link">Login</router-link>
          </div>
          <div class="navbar-item" v-if="!loggedIn">
            <router-link to="/register" class="nav-link">Register</router-link>
          </div>
          <div class="navbar-item" v-if="loggedIn">
            <router-link to="/logout" class="nav-link">Logout</router-link>
          </div>
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
}
</style>
