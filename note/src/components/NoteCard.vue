<template>
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <p class="text-gray-900 dark:text-white mb-4">{{ note.content }}</p>
        <small class="text-gray-500">Created: {{ new Date(note.created_at).toLocaleString() }}</small>
        <div class="mt-4 flex space-x-2">
            <button
                @click="openEditModal"
                class="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
            >
                Edit
            </button>
            <button
                @click="deleteNote"
                class="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
            >
                Delete
            </button>
        </div>
        <div
            v-if="isEditing"
            id="edit-modal"
            tabindex="-1"
            aria-hidden="true"
            class="fixed inset-0 z-50 overflow-y-auto overflow-x-hidden flex justify-center items-center bg-gray-900/50"
        >
            <div class="relative p-4 w-full max-w-2xl max-h-full">
                <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                    <div class="flex items-center justify-between p-4 border-b dark:border-gray-600">
                        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">Edit Note</h3>
                        <button
                            @click="isEditing = false"
                            class="text-gray-400 hover:bg-gray-200 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center dark:hover:bg-gray-600"
                        >
                            <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                            </svg>
                        </button>
                    </div>
                    <div class="p-4">
                        <textarea
                            v-model="editContent"
                            class="w-full p-2 border rounded dark:bg-gray-700 dark:text-white"
                            rows="4"
                        ></textarea>
                        <button
                            @click="saveNote"
                            class="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                        >
                            Save
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useNotesStore } from '../stores/notes'
import { toast } from 'vue3-toastify'

export default defineComponent({
    props: {
        note: {
            type: Object,
            required: true,
        },
    },
    setup(props) {
        const notesStore = useNotesStore()
        const isEditing = ref(false)
        const editContent = ref(props.note.content)

        const openEditModal = () => {
            isEditing.value = true
        }

        const saveNote = async () => {
            try {
                await notesStore.updateNote(props.note.id, editContent.value)
                isEditing.value = false
                toast.success('Note updated successfully')
            } catch (error: any) {
                toast.error(error.message || 'Failed to update note')
            }
        }

        const deleteNote = async () => {
            if (confirm('Are you sure you want to delete this note?')) {
                try {
                    await notesStore.deleteNote(props.note.id)
                    toast.success('Note deleted successfully')
                } catch (error: any) {
                    toast.error(error.message || 'Failed to delete note')
                }
            }
        }

        return { isEditing, editContent, openEditModal, saveNote, deleteNote }
    },
})
</script>