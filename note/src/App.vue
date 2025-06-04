<template>
  <v-app :theme="themeStore.isDark ? 'dark' : 'light'">
    <router-view />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useThemeStore } from './stores/theme'

export default defineComponent({
  name: 'App',
  setup() {
    const themeStore = useThemeStore()
    return { themeStore }
  },
})
</script>

<style scoped>
.v-application {
  transition: background-color 0.3s ease;
}
</style>