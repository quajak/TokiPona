<script setup lang="ts">
import { ref } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"

const error = ref("")
const username = ref("");
const password = ref("");

const router = useRouter()
const store = useStore()

async function register() {
    const result = await store.dispatch(ActionTypes.registerUser, {"username": username.value, "password": password.value})
    if(result["data"]["success"]){
        router.push("login")
        error.value = ""
    }
    else{
        error.value = result["data"]["error"];
    }
}
</script>

<template>
    <h1 class="title is-4">Register</h1>
    <div v-if="error != ''">
        <p>Error: {{ error }} </p>
    </div>
    <form @submit="register">
    <input class="input" v-model="username" placeholder="Username" style="width:15%; margin-right: 3%;">
    <input class="input" v-model="password" type="password" style="width:15%; margin-right: 3%;">
    <input class="button" type="submit" value="Submit">
    </form>
</template>

<style scoped lang="scss">
a {
  color: #42b983;
}

label {
  margin: 0 0.5em;
  font-weight: bold;
}

code {
  background-color: #eee;
  padding: 2px 4px;
  border-radius: 4px;
  color: #304455;
}
</style>
