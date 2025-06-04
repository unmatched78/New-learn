<template>
  <v-parallax
    src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg"
    height="100vh"
  >
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="6">
          <v-card class="pa-6 text-center" elevation="10">
            <v-card-title class="text-h4 justify-center">
              Welcome to NoteApp
            </v-card-title>
            <v-card-text>
              <p class="text-body-1">
                Organize your thoughts with our modern, intuitive note-taking app.
                Create, edit, and manage notes effortlessly.
              </p>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn
                color="primary"
                size="large"
                @click="router.push('/login')"
                prepend-icon="mdi-login"
              >
                Get Started
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-parallax>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const router = useRouter()
    return { router }
  },
})
</script>