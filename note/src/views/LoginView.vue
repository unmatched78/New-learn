<template>
  <div class="container mx-auto max-w-md p-4">
    <h2 class="text-2xl font-bold text-primary dark:text-white mb-4">Login</h2>
    <form @submit.prevent="login" class="space-y-4">
      <div>
        <label class="block text-gray-700 dark:text-gray-300">Username</label>
        <input
          v-model="form.username"
          type="text"
          class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
          required
        />
      </div>
      <div>
        <label class="block text-gray-700 dark:text-gray-300">Password</label>
        <input
          v-model="form.password"
          type="password"
          class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
          required
        />
      </div>
      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        :disabled="loading"
      >
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default defineComponent({
  name: 'LoginView',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const toast = useToast()
    const form = ref({ username: '', password: '' })
    const error = ref('')
    const loading = ref(false)

    const login = async () => {
      loading.value = true
      try {
        await userStore.login(form.value)
        toast.success('Logged in successfully')
        router.push('/notes')
      } catch (err: any) {
        error.value = err.message || 'Login failed'
        toast.error(error.value)
      } finally {
        loading.value = false
      }
    }

    return { form, login, error, loading }
  },
})
</script>