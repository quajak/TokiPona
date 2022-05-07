<script setup lang="ts">
import axios from 'axios'
import { ref, Ref } from 'vue'
import { useProgrammatic } from '@oruga-ui/oruga-next'
import { basePath } from '../api';

const { oruga } = useProgrammatic()

type Question = {
    english: string,
    toki: string,
    id: number
}

const settingMenu = ref(false);
const vocabMode = ref("All");
const question = ref(null) as Ref<Question|null>
const user_input = ref("");
let notification = null as any

async function getNextQuestion(){
    question.value = (await axios.get(basePath + "/api/get_vocab_pair", {params: {"mode": vocabMode.value}, withCredentials: true})).data as Question
}

async function evaluateAnswer(){
    if(question.value == null){
        return
    }
    let correct = user_input.value == question.value.toki
    let message = "Correct!";
    if(!correct){
        message = `<p> The correct answer is </p>
        <div>
            <a href="#/definition/${question.value.toki}" class="nav-link"> ${question.value.toki}</a> 
        </div>
        <p> You had written: ${user_input.value}</p>`
    }
    if(notification != null){
        notification.close();
    }
    const data = await axios.post(basePath + "/api/practise", {"vocab_id": question.value.id, "correct": correct, "type": 1}, {withCredentials: true}) as Record<string, any>
    user_input.value = ""
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
        </div>
    </o-modal>
    
    <button class="button" @click="settingMenu = true" style="position: absolute; bottom: 3%; left: 3%;"><i class="fa-solid fa-gear"></i></button>
    <div v-if="question != null" style="margin-top:10%">
        <p>Translate: {{ question.english }}</p>
        <form class="is-grouped-centered" style="margin-top: 20px" v-on:keyup.enter="evaluateAnswer">
            <input class="input is-small control" style="width: 200px" v-model="user_input">
            <button class="button is-small control" style="margin-left: 20px" type="button" @click="evaluateAnswer">Submit</button>
        </form>
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