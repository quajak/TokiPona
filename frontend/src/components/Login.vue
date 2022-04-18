<script setup lang="ts">
import { ref } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"

const error = ref("")
const username = ref("");
const password = ref("");

const { redirectReason } = defineProps<{redirectReason: string}>()

const router = useRouter()
const store = useStore()

async function login() {
    const result = await store.dispatch(ActionTypes.loginUser, {"username": username.value, "password": password.value})
    if(result["data"]["success"]){
        error.value = ""
        router.push("/")
    }
    else{
        error.value = result["data"]["error"];
    }
}
</script>

<template>
    <h1>Login</h1>
    <div v-if="error != ''">
        <p>Error: {{ error }} </p>
    </div>
    <form @submit="login">
    <input v-model="username" placeholder="Username">
    <input v-model="password" type="password">
    <input type="submit" value="Submit">
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
