import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    isDark: ref(false),
  }),
  actions: {
    toggleTheme() {
      this.isDark = !this.isDark
    },
  },
})