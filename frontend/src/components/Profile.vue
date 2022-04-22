<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"
import axios from 'axios';
import { basePath } from '../api';

const currentStreak = ref(0)
const bestStreak = ref(0);
const progress = ref(0);

const store = useStore()

onMounted(async () => {
    const response = await axios.get(basePath + "/api/profile", {withCredentials: true})
    currentStreak.value = response.data["current"]
    bestStreak.value = response.data["best"]
    progress.value = response.data["progress"]
})

</script>

<template>
    <h1 class="title is-4">Profile: {{store.state.user.data["username"] }}</h1>
    <p>Current streak: {{ currentStreak }}</p>
    <p>Highest streak: {{ bestStreak }}</p>
    <p>Progress: {{ progress }} </p>
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
