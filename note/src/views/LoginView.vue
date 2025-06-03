<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify';
import { useForm, useField } from 'vee-validate'
import { defineRule } from 'vee-validate'
import { required, min } from '@vee-validate/rules'

defineRule('required', required)
defineRule('min', min)

export default defineComponent({
  name: 'LoginView',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const toast = useToast()
    const { handleSubmit, errors } = useForm()
    const { value: username } = useField('username', 'required')
    const { value: password } = useField('password', 'required|min:8')
    const loading = ref(false)

    const login = handleSubmit(async () => {
      loading.value = true
      try {
        await userStore.login({ username: username.value, password: password.value })
        toast.success('Logged in successfully')
        router.push('/notes')
      } catch (err: any) {
        toast.error(err.message || 'Login failed')
      } finally {
        loading.value = false
      }
    })

    return { username, password, login, errors, loading }
  },
})
</script>
<template>
  <div class="container mx-auto max-w-md p-4">
    <h2 class="text-2xl font-bold text-primary dark:text-white mb-4">Login</h2>
    <form @submit="login" class="space-y-4">
      <div>
        <label class="block text-gray-700 dark:text-gray-300">Username</label>
        <input
          v-model="username"
          type="text"
          class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
        />
        <p v-if="errors.username" class="text-red-500">{{ errors.username }}</p>
      </div>
      <div>
        <label class="block text-gray-700 dark:text-gray-300">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
        />
        <p v-if="errors.password" class="text-red-500">{{ errors.password }}</p>
      </div>
      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        :disabled="loading"
      >
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
    </form>
  </div>
</template>