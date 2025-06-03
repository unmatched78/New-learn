<template>
  <div class="container mx-auto p-4">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-2xl font-bold text-primary dark:text-white">My Notes</h2>
      <button
        @click="logout"
        class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
      >
        Logout
      </button>
    </div>
    <div class="mb-4">
      <QuillEditor
        v-model:content="newNote"
        contentType="html"
        theme="snow"
        class="w-full bg-white dark:bg-gray-700"
      />
      <button
        @click="createNote"
        class="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        :disabled="loading"
      >
        <PlusIcon class="w-5 h-5 inline mr-2" /> Add Note
      </button>
    </div>
    <div v-if="loading" class="text-center text-gray-600 dark:text-gray-300">Loading...</div>
    <div v-else-if="notes.length === 0" class="text-center text-gray-600 dark:text-gray-300">
      No notes yet. Create one!
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <NoteCard v-for="note in notes" :key="note.id" :note="note" />
    </div>
    <p v-if="error" class="text-red-500 mt-4">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useNotesStore } from '../stores/notes'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify';
import { QuillEditor } from '@vueup/vue-quill'
import { PlusIcon } from '@heroicons/vue/24/solid'
import NoteCard from '../components/NoteCard.vue'

export default defineComponent({
  components: { QuillEditor, PlusIcon, NoteCard },
  setup() {
    const notesStore = useNotesStore()
    const userStore = useUserStore()
    const router = useRouter()
    const toast = useToast()
    const newNote = ref('')
    const error = ref('')
    const loading = ref(false)

    const fetchNotes = async () => {
      loading.value = true
      try {
        await notesStore.fetchNotes()
      } catch (err: any) {
        error.value = err.message || 'Failed to fetch notes'
        toast.error(error.value)
      } finally {
        loading.value = false
      }
    }

    const createNote = async () => {
      if (!newNote.value.trim()) {
        toast.error('Note content cannot be empty')
        return
      }
      loading.value = true
      try {
        await notesStore.createNote(newNote.value)
        newNote.value = ''
        toast.success('Note created successfully')
      } catch (err: any) {
        error.value = err.message || 'Failed to create note'
        toast.error(error.value)
      } finally {
        loading.value = false
      }
    }

    const logout = () => {
      userStore.logout()
      toast.info('Logged out')
      router.push('/login')
    }

    onMounted(fetchNotes)

    return { notes: notesStore.notes, newNote, createNote, logout, error, loading }
  },
})
</script>