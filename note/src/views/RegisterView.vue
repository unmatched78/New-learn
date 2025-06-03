<template>
  <div class="container mx-auto max-w-md p-4">
    <h2 class="text-2xl font-bold text-primary dark:text-white mb-4">Register</h2>
    <form @submit.prevent="register" class="space-y-4">
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
      <div>
        <label class="block text-gray-700 dark:text-gray-300">Confirm Password</label>
        <input
          v-model="form.password2"
          type="password"
          class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
          required
        />
      </div>
      <div>
        <label class="block text-gray-700 dark:text-gray-300">Role</label>
        <select
          v-model="form.role"
          class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
        >
          <option value="boy">Boy</option>
          <option value="girl">Girl</option>
        </select>
      </div>
      <button
        type="submit"
        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        :disabled="loading"
      >
        {{ loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify';

export default defineComponent({
  name: 'RegisterView',
  setup() {
    const userStore = useUserStore()
    const router = useRouter()
    const toast = useToast()
    const form = ref({ username: '', password: '', password2: '', role: 'boy' })
    const error = ref('')
    const loading = ref(false)

    const register = async () => {
      loading.value = true
      try {
        await userStore.register(form.value)
        toast.success('Registered successfully')
        router.push('/notes')
      } catch (err: any) {
        error.value = err.message || 'Registration failed'
        toast.error(error.value)
      } finally {
        loading.value = false
      }
    }

    return { form, register, error, loading }
  },
})
</script>