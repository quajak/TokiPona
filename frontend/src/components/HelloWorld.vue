<script setup lang="ts">
import { ref } from 'vue'

</script>

<template>
  <h1 class="title is-5">Toki!</h1>
  <p>I made this website to help me learn the conlanguage Toki Pona. I hope it can help you as well! Simply register an account to start practising!</p>
  <p style="margin-top:20px">All credit goes to Sonja Lang for creating the language and to Jan Lope for his <a href="https://jan-lope.github.io/Toki_Pona_lessons_English/">resources</a>, espeically the dictionary.</p>
  <p style="margin-top:5px">The code for this website is open source and can be found on <a href="https://github.com/quajak/TokiPona">github</a>. Any feedback is appreciated!</p>
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
