<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <div class="toggle-container">
      <DarkModeToggle @update:darkMode="toggleDarkMode"/>
    </div>
    <GPTChat/>
  </div>
</template>

<script>
import DarkModeToggle from './components/DarkModeToggle.vue';
import GPTChat from "@/components/GPTChat.vue";

export default {
  name: 'App',
  components: {
    GPTChat,
    DarkModeToggle
  },
  data() {
    return {
      isDarkMode: false
    }
  },
  methods: {
    toggleDarkMode() {
      document.body.classList.toggle('dark-mode');
    }
  }
}
</script>

<style>
.toggle-container {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 1000;
}


</style>
