<script setup lang="ts">
import axios from 'axios'
import { ref, Ref } from 'vue'
import { useProgrammatic } from '@oruga-ui/oruga-next'
import { basePath } from '../api';

const { oruga } = useProgrammatic()

type Question = {
    correct_english: Array<string>,
    other_options: Array<string>,
    toki: string
}

type Option = {
    word: string,
    correct: boolean,
    selected: boolean,
    hidden: boolean
}

const question = ref(null) as Ref<Question|null>
const options = ref([]) as Ref<Array<Option>>
const buttonText = ref("Submit")

// https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffleArray<T>(array: Array<T>) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]
    }
}

async function getNextQuestion(){
    question.value = (await axios.get(basePath + "/api/selectall", {withCredentials: true})).data as Question
    if(question.value != null){
        options.value = question.value.other_options.map(o => {return {word: o, correct: false, selected: false, hidden: true} as Option})
                            .concat(question.value.correct_english.map(o => {return {word: o, correct: true, selected: false, hidden: true} as Option}))
        shuffleArray(options.value)
    }   

}

async function showAnswer(){
    options.value.forEach(element => {
        element.hidden = false
    });
}

async function progress(){
    if(options.value[0].hidden){
        await showAnswer()
        buttonText.value = "Next"
    }
    else{
        await getNextQuestion()
        buttonText.value = "Submit"
    }
}
</script>

<template>
    <div v-if="question != null" style="margin-top:10%">
        <p style="font-weight: bold">Nimi: {{ question.toki }}</p>
        <div v-for="index in 4" :key="index">
            <div class="buttons level container" style="width:35%; margin-top: 20px">
                <button v-for="option in options.slice((index-1) * 5, index * 5)" 
                    :class='["button", "is-outlined", (option.selected && option.hidden) ? "is-info" : "",
                    (!option.hidden && option.correct != option.selected) ? "is-danger" : "",
                    (!option.hidden && option.correct == option.selected) ? "is-primary" : ""]' @click="() => option.selected = !option.selected">
                    {{option.word}}
                </button>
            </div>
        </div>
        <button class="button is-info" @click="progress">{{buttonText}}</button>
    </div>
    <div v-else>
        <button class="button is-info" @click="getNextQuestion">Start</button>
    </div>
</template>