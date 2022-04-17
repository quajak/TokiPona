<script setup lang="ts">
import { ref } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"

const router = useRouter()
const store = useStore()

function logout(){
  store.dispatch(ActionTypes.logoutUser)
  router.push("/")
}
</script>

<template>
    <button @click="logout">Logout</button>
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
