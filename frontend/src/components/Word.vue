<script setup lang="ts">
import { ref, onMounted, computed, ComputedRef, watch, toRefs } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"
import axios from 'axios'
import { basePath } from '../api'

const store = useStore()

const props = defineProps<{ word: string}>()

</script>

<template>
    <h4 class="title is-4" style="margin: 0px">{{ props.word }}</h4>
    <div v-for="definition in store.getters.defintionFor(props.word)">
        <span style="font-weight: bold; padding-right: 4px">{{ definition.type }}: </span>
        <span v-for="english in definition.english" style="padding-right: 9px;">
            {{ english }}
        </span>
    </div>
    <div style="margin-bottom: 10px;"></div>
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
