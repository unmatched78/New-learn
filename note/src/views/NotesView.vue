<template>
    <div class="container mx-auto p-4">
        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold text-primary dark:text-white">My Notes</h2>
            <!-- <button
                    @click="fetchNotes"
                    class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                    Refresh
                </button> -->
            <button
                @click="logout"
                class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
                Logout
            </button>
        </div>
        
        <div class="mb-4">
            <textarea
                v-model="newNote"
                placeholder="Write your note here..."
                class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                rows="4"
            ></textarea>
            <button
                @click="createNote"
                class="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex items-center"
                :disabled="loading"
            >
                <PlusIcon class="w-5 h-5 mr-2" /> {{ loading ? 'Creating...' : 'Add Note' }}
            </button>
        </div>
        <div v-if="loading" class="text-center text-gray-600 dark:text-gray-300">Loading...</div>
        <div v-else-if="notes.length === 0" class="text-center text-gray-600 dark:text-gray-300">
            No notes yet. Create one!
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <NoteCard v-for="note in notes" :key="note.id" :note="note" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useNotesStore } from '../stores/notes'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'
import { toast } from 'vue3-toastify'
import { PlusIcon } from '@heroicons/vue/24/solid'
import NoteCard from '../components/NoteCard.vue'

export default defineComponent({
    components: { PlusIcon, NoteCard },
    setup() {
        const notesStore = useNotesStore()
        const userStore = useUserStore()
        const router = useRouter()
        const newNote = ref('')
        const loading = ref(false)

        const notes = computed(() => {
            console.log('Computed notes:', notesStore.notes)
            return notesStore.notes
        })

        const fetchNotes = async () => {
            loading.value = true
            try {
                await notesStore.fetchNotes()
            } catch (err: any) {
                toast.error(err.message || 'Failed to fetch notes')
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
                toast.error(err.message || 'Failed to create note')
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

        return { notes, newNote, createNote, logout, loading }
    },
})
</script>