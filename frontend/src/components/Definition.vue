<script setup lang="ts">
import { ref } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"
import axios from 'axios';
import { basePath } from '../api';
import Word from "./Word.vue"

</script>

<template>
    <Word :word="($route.params.word as string)"></Word>
</template>

<style scoped lang="scss">

</style>
