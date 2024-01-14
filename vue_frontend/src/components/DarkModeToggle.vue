<template>
  <button @click="toggleDarkMode" class="btn btn-dark btn-sm">Toggle Dark Mode</button>
</template>

<script>
export default {
  emits: ['update:darkMode'],
  methods: {
    toggleDarkMode() {
      this.$emit('update:darkMode');
    }
  }
}
</script>
