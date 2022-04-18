<script setup lang="ts">
import axios from 'axios'
import { ref, Ref } from 'vue'
import { useProgrammatic } from '@oruga-ui/oruga-next'

const { oruga } = useProgrammatic()

type Question = {
    correct_english: string,
    other_options: Array<string>,
    toki: string,
    vocab_id: number
}

const question = ref(null) as Ref<Question|null>
const options = ref([] as Array<string>)
let notification = null as any
let correctCount = 0

// https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffleArray<T>(array: Array<T>) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]
    }
}

async function getNextQuestion(){
    question.value = (await axios.get("/api/vocab", {withCredentials: true})).data as Question
    if(question.value != null){
        options.value = question.value.other_options
        options.value.push(question.value.correct_english)
        shuffleArray(options.value)
    }

}

async function selectAnswer(chosen: string){
    if(question.value == null){
        return
    }
    let correct = chosen == question.value.correct_english
    let message = "Correct!";
    if(!correct){
        message = question.value.toki + " = " + question.value.correct_english + " (You chose: " + chosen + ")"
        correctCount = 0
    }
    else{
        correctCount++
        message += " x" + correctCount
    }
    if(notification != null){
        notification.close();
    }
    notification = oruga.notification.open({
        message: message,
        variant: correct ? "success" : "danger",
        position: "top",
        duration: 600,
        indefinite: !correct,
        closable: true
    })
    await axios.post("/api/practise", {"vocab_id": question.value.vocab_id, "correct": correct}, {withCredentials: true})
    await getNextQuestion()
}
</script>

<template>
    <div v-if="question != null" style="margin-top:10%">
        <p>Nimi: {{ question.toki }}</p>
        <div class="buttons level container" style="width:35%; margin-top: 20px">
            <button class="button" v-for="option in options" @click="() => selectAnswer(option)">
                {{option}}
            </button>
        </div>
    </div>
    <div v-else>
        <button class="button is-info" @click="getNextQuestion">Start</button>
    </div>
</template>

<style scoped lang="scss">
</style>
