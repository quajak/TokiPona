<script setup lang="ts">
import axios from 'axios'
import { ref, Ref } from 'vue'
import { useProgrammatic } from '@oruga-ui/oruga-next'
import { basePath } from '../api';

const { oruga } = useProgrammatic()

type Question = {
    correct_english: string,
    other_options: Array<string>,
    toki: string,
    vocab_id: number
}

const settingMenu = ref(false);
const vocabMode = ref("All");
const vocabOptions = ref(4);
const question = ref(null) as Ref<Question|null>
const options = ref([] as Array<string>)
let notification = null as any

// https://stackoverflow.com/questions/2450954/how-to-randomize-shuffle-a-javascript-array
function shuffleArray<T>(array: Array<T>) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]
    }
}

async function getNextQuestion(){
    question.value = (await axios.get(basePath + "/api/vocab", {params: {"mode": vocabMode.value, "options": vocabOptions.value}, withCredentials: true})).data as Question
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
        message = `<p>${question.value.toki} = ${question.value.correct_english}</p> 
        <div>
            <a href="#/definition/${question.value.toki}" class="nav-link">See ${question.value.toki} definition</a> 
        </div>
        <p> You had chosen: ${chosen}</p>`
    }
    if(notification != null){
        notification.close();
    }
    const data = await axios.post(basePath + "/api/practise", {"vocab_id": question.value.vocab_id, "correct": correct, "type": 0}, {withCredentials: true}) as Record<string, any>
    
    if(data.data["streak"] != 0){
        message += " x" + data.data["streak"]
    }

    notification = oruga.notification.open({
        message: message,
        variant: correct ? "success" : "danger",
        position: "top",
        duration: 600,
        indefinite: !correct,
        closable: true
    })
    await getNextQuestion()
}
</script>

<template>
    <o-modal v-model:active="settingMenu">
        <div style="z-index: 50; background-color: white; padding: 30px; border-radius: 15%;">
            <h4>Settings</h4>
            <o-field label="Mode">
                <o-select placeholder="Select a mode" v-model="vocabMode">
                    <option value="All">All words</option>
                    <option value="Mistakes">Revise mistakes</option>
                </o-select>
            </o-field>
            <o-field label="Options">
                <o-select placeholder="Select number of options" v-model="vocabOptions">
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                </o-select>
            </o-field>
        </div>
    </o-modal>
    
    <button class="button" @click="settingMenu = true" style="position: absolute; bottom: 3%; left: 3%;"><i class="fa-solid fa-gear"></i></button>
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

<style>
.modal-background{
    z-index: -1;
}
</style>