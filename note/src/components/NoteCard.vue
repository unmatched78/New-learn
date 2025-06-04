<template>
  <v-card class="ma-2 pa-4">
    <v-card-text>
      <p class="text-body-1">{{ note.content }}</p>
      <p class="text-caption text-grey">
        Created: {{ new Date(note.created_at).toLocaleString() }}
      </p>
    </v-card-text>
    <v-card-actions>
      <v-btn
        icon="mdi-pencil"
        variant="text"
        @click="openEditModal"
        size="small"
      ></v-btn>
      <v-btn
        icon="mdi-delete"
        variant="text"
        color="error"
        @click="deleteNote"
        size="small"
      ></v-btn>
    </v-card-actions>

    <v-dialog v-model="isEditing" max-width="600px">
      <v-card>
        <v-card-title>Edit Note</v-card-title>
        <v-card-text>
          <v-textarea
            v-model="editContent"
            label="Note content"
            rows="4"
            variant="outlined"
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="isEditing = false">Cancel</v-btn>
          <v-btn color="primary" @click="saveNote" :loading="loading">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useNotesStore } from '../stores/notes'

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
    const loading = ref(false)

    const openEditModal = () => {
      isEditing.value = true
    }

    const saveNote = async () => {
      loading.value = true
      try {
        await notesStore.updateNote(props.note.id, editContent.value)
        isEditing.value = false
      } catch (error: any) {
        console.error('Update note error:', error)
      } finally {
        loading.value = false
      }
    }

    const deleteNote = async () => {
      if (confirm('Are you sure you want to delete this note?')) {
        try {
          await notesStore.deleteNote(props.note.id)
        } catch (error: any) {
          console.error('Delete note error:', error)
        }
      }
    }

    return { isEditing, editContent, openEditModal, saveNote, deleteNote, loading }
  },
})
</script>