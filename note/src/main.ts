import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import './assets/main.css'
import 'flowbite' // Flowbite JavaScript
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Toast, { timeout: 3000 })
app.mount('#app')