<template>
  <v-container fluid class="pa-4">
    <v-row>
      <!-- Sidebar -->
      <v-navigation-drawer v-model="drawer" app width="300">
        <v-list>
          <v-list-item>
            <v-list-item-title class="text-h6">Notes</v-list-item-title>
          </v-list-item>
          <v-list-item
            v-for="note in notes"
            :key="note.id"
            @click="selectNote(note)"
            :class="{ 'v-list-item--active': selectedNote?.id === note.id }"
          >
            <v-list-item-title>{{ truncate(note.content, 20) }}</v-list-item-title>
            <v-list-item-subtitle>{{
              new Date(note.created_at).toLocaleString()
            }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>

      <!-- Main content -->
      <v-main>
        <v-toolbar flat>
          <v-toolbar-title class="text-h5">My Notes</v-toolbar-title>
          <v-spacer />
          <v-btn icon @click="drawer = !drawer" class="d-md-none">
            <v-icon>mdi-menu</v-icon>
          </v-btn>
          <v-btn
            :icon="themeStore.isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'"
            @click="themeStore.toggleTheme"
          ></v-btn>
          <v-btn color="error" @click="logout">Logout</v-btn>
        </v-toolbar>

        <!-- Note creation -->
        <v-card class="ma-4 pa-4">
          <v-form @submit.prevent="createNote">
            <v-textarea
              v-model="newNote"
              label="Write your note here..."
              rows="4"
              variant="outlined"
              :disabled="loading"
            ></v-textarea>
            <v-btn
              color="primary"
              type="submit"
              :loading="loading"
              :disabled="!newNote.trim()"
              prepend-icon="mdi-plus"
            >
              Add Note
            </v-btn>
          </v-form>
        </v-card>

        <!-- Notes table -->
        <v-card class="ma-4">
          <v-data-table
            :items="notes"
            :headers="headers"
            :loading="loading"
            :sort-by="[{ key: 'created_at', order: 'desc' }]"
            :items-per-page="10"
            show-current-page
          >
            <template v-slot:item.content="{ item }">
              <span class="truncate">{{ item.content }}</span>
            </template>
            <template v-slot:item.created_at="{ item }">
              {{ new Date(item.created_at).toLocaleString() }}
            </template>
            <template v-slot:item.actions="{ item }">
              <v-btn
                icon="mdi-pencil"
                variant="text"
                @click="openEditModal(item)"
                size="small"
              ></v-btn>
              <v-btn
                icon="mdi-delete"
                variant="text"
                color="error"
                @click="deleteNote(item.id)"
                size="small"
              ></v-btn>
            </template>
            <template v-slot:no-data>
              <v-alert type="info">No notes yet. Create one!</v-alert>
            </template>
          </v-data-table>
        </v-card>

        <!-- Edit dialog -->
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
      </v-main>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useNotesStore } from '../stores/notes'
import { useUserStore } from '../stores/user'
import { useThemeStore } from '../stores/theme'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const notesStore = useNotesStore()
    const userStore = useUserStore()
    const themeStore = useThemeStore()
    const router = useRouter()
    const newNote = ref('')
    const loading = ref(false)
    const drawer = ref(true)
    const selectedNote = ref(null)
    const isEditing = ref(false)
    const editContent = ref('')
    const editNoteId = ref(0)

    const notes = computed(() => notesStore.notes)
    const headers = [
      { title: 'Content', key: 'content', sortable: true },
      { title: 'Created', key: 'created_at', sortable: true },
      { title: 'Actions', key: 'actions', sortable: false },
    ]

    const fetchNotes = async () => {
      loading.value = true
      try {
        await notesStore.fetchNotes()
      } catch (err: any) {
        console.error('Fetch notes error:', err)
      } finally {
        loading.value = false
      }
    }

    const createNote = async () => {
      if (!newNote.value.trim()) return
      loading.value = true
      try {
        await notesStore.createNote(newNote.value)
        newNote.value = ''
      } catch (err: any) {
        console.error('Create note error:', err)
      } finally {
        loading.value = false
      }
    }

    const openEditModal = (note: any) => {
      editNoteId.value = note.id
      editContent.value = note.content
      isEditing.value = true
    }

    const saveNote = async () => {
      loading.value = true
      try {
        await notesStore.updateNote(editNoteId.value, editContent.value)
        isEditing.value = false
      } catch (err: any) {
        console.error('Update note error:', err)
      } finally {
        loading.value = false
      }
    }

    const deleteNote = async (id: number) => {
      if (confirm('Are you sure you want to delete this note?')) {
        loading.value = true
        try {
          await notesStore.deleteNote(id)
        } catch (err: any) {
          console.error('Delete note error:', err)
        } finally {
          loading.value = false
        }
      }
    }

    const selectNote = (note: any) => {
      selectedNote.value = note
    }

    const truncate = (text: string, length: number) =>
      text.length > length ? text.slice(0, length) + '...' : text

    const logout = () => {
      userStore.logout()
      router.push('/login')
    }

    onMounted(fetchNotes)

    return {
      notes,
      newNote,
      loading,
      drawer,
      selectedNote,
      isEditing,
      editContent,
      headers,
      selectNote,
      truncate,
      createNote,
      openEditModal,
      saveNote,
      deleteNote,
      fetchNotes,
      logout,
      themeStore,
    }
  },
})
</script>

<style scoped>
.truncate {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>