<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold text-primary dark:text-white">Welcome to Note Taker</h1>
    <p class="mt-4 text-gray-600 dark:text-gray-300">
      Log in or register to start taking notes!
    </p>
    <div class="mt-4 space-x-4">
      <router-link
        to="/login"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Login
      </router-link>
      <router-link
        to="/register"
        class="bg-secondary text-white px-4 py-2 rounded hover:bg-gray-700"
      >
        Register
      </router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'HomeView',
})
</script>