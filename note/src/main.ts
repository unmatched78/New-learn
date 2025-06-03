import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Vue3Toastify from 'vue3-toastify';
// Use Vue3Toastify as needed
//import { Vue3Toastify } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css'; // Import the styles
import './style.css'; // Your custom styles
import 'flowbite'; // Assuming you’re using Flowbite
const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(Vue3Toastify, { autoClose: 3000 }); // Configure toast duration
app.mount('#app');