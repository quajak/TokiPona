<script setup lang="ts">
import { ref } from 'vue'
import { mapActions, mapGetters, useStore } from 'vuex'
import { ActionTypes } from '../store/store'
import { useRouter} from "vue-router"
import axios from 'axios';
import { basePath } from '../api';
import Word from "./Word.vue"

const words = ref([] as Array<string>)
const number = ref(10)
const searchTerm = ref("")

async function getWords(search: string) {
    searchTerm.value = search
    const result = await axios.get(basePath + "/api/dictionary/search", {params: {"word": searchTerm.value}, withCredentials: true})
    words.value = result.data["results"]
    number.value = 10
}

function onlyUnique(value: any, index: int, self: Array<any>) {
  return self.indexOf(value) === index;
}

getWords("")
</script>

<template>
    <h1 class="title is-4">Dictionary</h1>
    <div class="container" style="width:25%;">
      <o-field label="SearchTerm">
        <o-input v-model="searchTerm" @input="getWords($event.target.value)" @update="getWords($event.target.value)" ></o-input>
      </o-field>
    </div>
    <div class="level container" style="width: 50%">
      <div class="level-item">
        <button class="button" style="margin: 3px" v-for="letter in words.filter(w => w.length > searchTerm.length).map(w => w[searchTerm.length]).filter(onlyUnique)" @click="getWords(searchTerm + letter)">{{letter}}</button>
      </div>
    </div>
    <Word v-for="word in words.slice(0, number)" :word="word" :key="word"></Word>
    <button class="button" style="margin-bottom: 5%" v-if="number<words.length" @click="number += 5">More</button>
</template>

<style scoped lang="scss">

</style>
