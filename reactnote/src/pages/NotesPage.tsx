// src/pages/NotesPage.tsx
import React, { useEffect, useState } from "react";
import api from "@/api/api"; // your Axios instance with JWT interceptor
import { useAuth } from "../context/AuthContext";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ModeToggle } from "@/components/mode-toggle";
import { toast } from "react-hot-toast";

interface Note {
  id: number;
  content: string;
  created_at: string;
  updated_at: string;
  // `notewriter` is read-only in serializer, omitted here
}

export default function NotesPage() {
  const { user, logout } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [editorContent, setEditorContent] = useState<string>("");
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isLoadingNotes, setIsLoadingNotes] = useState<boolean>(true);

  // 1) Fetch all notes on mount
  useEffect(() => {
    async function fetchNotes() {
      setIsLoadingNotes(true);
      try {
        const response = await api.get<Note[]>("/notes/");
        setNotes(response.data);
        // If there is at least one note, select the first by default:
        if (response.data.length > 0) {
          setSelectedNote(response.data[0]);
          setEditorContent(response.data[0].content);
        }
      } catch (err) {
        toast.error("Failed to load notes.");
      } finally {
        setIsLoadingNotes(false);
      }
    }
    fetchNotes();
  }, []);

  // 2) When the selected note changes, update the textarea content
  useEffect(() => {
    if (selectedNote) {
      setEditorContent(selectedNote.content);
    } else {
      setEditorContent("");
    }
  }, [selectedNote]);

  // 3) Create a brand‐new blank note
  async function handleNewNote() {
    try {
      const response = await api.post<Note>("/notes/", { content: "" });
      const newNote = response.data;
      // Add to our local notes list and select it
      setNotes((prev) => [newNote, ...prev]);
      setSelectedNote(newNote);
      setEditorContent("");
    } catch (err) {
      toast.error("Could not create a new note.");
    }
  }

  // 4) Save changes to the currently selected note
  async function handleSaveNote() {
    if (!selectedNote) {
      return;
    }
    setIsSaving(true);
    try {
      const response = await api.put<Note>(`/notes/${selectedNote.id}/`, {
        content: editorContent,
      });
      const updated = response.data;
      // Update it in the notes array
      setNotes((prev) =>
        prev.map((n) => (n.id === updated.id ? updated : n))
      );
      setSelectedNote(updated);
      toast.success("Saved.");
    } catch (err) {
      toast.error("Failed to save note.");
    } finally {
      setIsSaving(false);
    }
  }

  // 5) Delete the currently selected note
  async function handleDeleteNote() {
    if (!selectedNote) {
      return;
    }
    const idToDelete = selectedNote.id;
    try {
      await api.delete(`/notes/${idToDelete}/`);
      toast.success("Deleted.");
      // Remove from local list
      setNotes((prev) => prev.filter((n) => n.id !== idToDelete));
      // If there are still notes left, select the first one, otherwise nullify
      setSelectedNote((prev) => {
        const remaining = notes.filter((n) => n.id !== idToDelete);
        if (remaining.length > 0) {
          setEditorContent(remaining[0].content);
          return remaining[0];
        } else {
          setEditorContent("");
          return null;
        }
      });
    } catch (err) {
      toast.error("Failed to delete note.");
    }
  }

  // 6) Switch selection when user clicks a note in the sidebar
  function handleSelectNote(note: Note) {
    setSelectedNote(note);
    // editorContent will be updated automatically by useEffect above
  }

  return (
    <div className="h-screen flex">
      {/* ───────────────────────────────────────────────────────────────────── Sidebar ───────────────────────────────────────────────────────────────────── */}
      <aside className="w-64 border-r border-gray-200 dark:border-gray-700 flex flex-col">
        <div className="px-4 py-3 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold">Your Notes</h2>
          <Button size="icon" variant="outline" onClick={handleNewNote}>
            +{/* you can put a plus icon if you want */}
          </Button>
        </div>

        <ScrollArea className="flex-1 px-2 py-2">
          {isLoadingNotes ? (
            <p className="text-center text-sm text-gray-500">Loading…</p>
          ) : notes.length === 0 ? (
            <p className="text-center text-sm text-gray-500">
              No notes yet. Click “+” to create one.
            </p>
          ) : (
            <ul className="space-y-1">
              {notes.map((note) => (
                <li key={note.id}>
                  <button
                    onClick={() => handleSelectNote(note)}
                    className={`w-full text-left px-3 py-2 rounded-md transition 
                      ${
                        selectedNote?.id === note.id
                          ? "bg-gray-200 dark:bg-gray-700"
                          : "hover:bg-gray-100 dark:hover:bg-gray-800"
                      }`}
                  >
                    {/* Show first 20 chars of content, or “(empty)” if it’s blank */}
                    <span className="block truncate">
                      {note.content.trim() !== ""
                        ? note.content.slice(0, 20) +
                          (note.content.length > 20 ? "…" : "")
                        : "(empty)"}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {new Date(note.updated_at).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </ScrollArea>
      </aside>

      {/* ──────────────────────────────────────────────────────────────────── Main Editor Area ─────────────────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col">
        {/* Header with ModeToggle + Logout */}
        <header className="px-6 py-4 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
          <ModeToggle />
          <Button variant="ghost" size="sm" onClick={logout}>
            Log out
          </Button>
        </header>

        {/* If no note is selected, show a placeholder */}
        {!selectedNote ? (
          <div className="flex-1 flex items-center justify-center">
            <p className="text-gray-500">Select or create a note to get started.</p>
          </div>
        ) : (
          <div className="flex-1 p-6 flex flex-col">
            {/* Editor */}
            <Textarea
              className="flex-1 resize-none rounded-md border border-gray-300 dark:border-gray-600 p-4 focus:ring-2 focus:ring-indigo-500 focus:outline-none dark:bg-gray-800 dark:text-gray-100"
              placeholder="Type your note here..."
              value={editorContent}
              onChange={(e) => setEditorContent(e.target.value)}
            />

            <div className="mt-4 flex justify-end space-x-2">
              <Button
                variant="destructive"
                size="sm"
                onClick={handleDeleteNote}
                disabled={isSaving}
              >
                Delete
              </Button>
              <Button
                size="sm"
                onClick={handleSaveNote}
                disabled={isSaving}
              >
                {isSaving ? "Saving…" : "Save"}
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
