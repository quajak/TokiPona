<script setup lang="ts">
import { ref, Ref, onMounted } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"
import axios from 'axios';
import { basePath } from '../api';

type StreakInfo = {
  best: number,
  current: number,
  name: string
}

const streaks = ref([]) as Ref<Array<StreakInfo>>
const progress = ref(0);

const store = useStore()


onMounted(async () => {
    const response = (await axios.get(basePath + "/api/profile", {withCredentials: true})).data
    streaks.value = [
      {name: "Match English", best: response.scores["0"].best, current: response.scores["0"].current},
      {name: "Type Toki", best: response.scores["1"].best, current: response.scores["1"].current}
    ]
    progress.value = response["progress"]
})

</script>

<template>
    <h1 class="title is-4">Profile: {{store.state.user.data["username"] }}</h1>
    <p style="margin-top: 20px">Overall Progress: {{ progress }}</p>
    <p class="title is-5" style="margin-top:12px; margin-bottom: 8px">Streaks</p>
    <div v-for="streak in streaks">
      <p class="title is-6" style="margin-bottom:0px; margin-top: 10px"> {{ streak.name }} </p>
      <p>Current streak: {{ streak.current }}</p>
      <p>Highest streak: {{ streak.best }}</p>
    </div>
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
