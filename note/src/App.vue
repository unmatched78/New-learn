<template>
  <div :class="['min-h-screen', darkMode ? 'dark' : '']">
    <div class="fixed top-4 right-4">
      <button
        @click="toggleDarkMode"
        class="p-2 rounded bg-gray-200 dark:bg-gray-700"
      >
        <SunIcon v-if="darkMode" class="w-6 h-6 text-yellow-400" />
        <MoonIcon v-else class="w-6 h-6 text-gray-800" />
      </button>
    </div>
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { SunIcon, MoonIcon } from '@heroicons/vue/24/solid'

export default defineComponent({
  name: 'App',
  components: { SunIcon, MoonIcon },
  setup() {
    const darkMode = ref(localStorage.getItem('theme') === 'dark')
    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value
      localStorage.setItem('theme', darkMode.value ? 'dark' : 'light')
      document.documentElement.classList.toggle('dark', darkMode.value)
    }
    if (darkMode.value) {
      document.documentElement.classList.add('dark')
    }
    return { darkMode, toggleDarkMode }
  },
})
</script>