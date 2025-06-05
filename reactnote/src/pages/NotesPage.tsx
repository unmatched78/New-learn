// src/pages/NotesPage.tsx

import React, { useEffect, useRef, useState } from "react";
import api from "@/api/api"; // Axios instance with JWT interceptor
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
}

export default function NotesPage() {
  const { user, logout } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [editorContent, setEditorContent] = useState<string>("");

  // NEW STATE: Are we in “create new note” mode?
  const [isCreatingNew, setIsCreatingNew] = useState<boolean>(false);
  const [newContent, setNewContent] = useState<string>("");

  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isLoadingNotes, setIsLoadingNotes] = useState<boolean>(true);

  // ─── 1) Fetch all notes on mount ─────────────────────────────────────────────
  useEffect(() => {
    async function fetchNotes() {
      setIsLoadingNotes(true);
      try {
        const response = await api.get<Note[]>("/notes/");
        setNotes(response.data);
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

  // ─── 2) Sync selectedNote → editorContent (only when editing existing) ────
  useEffect(() => {
    if (!isCreatingNew && selectedNote) {
      setEditorContent(selectedNote.content);
    }
  }, [selectedNote, isCreatingNew]);

  // ─── 3) Handler for clicking “+” (start new note) ─────────────────────────
  function handleStartNew() {
    setIsCreatingNew(true);
    setNewContent(""); // blank draft
    setSelectedNote(null);
    setEditorContent("");
  }

  // ─── 4) Cancel new-note creation ───────────────────────────────────────────
  function handleCancelNew() {
    setIsCreatingNew(false);
    setNewContent("");
    // If there was a previously selected note, restore it
    if (notes.length > 0) {
      setSelectedNote(notes[0]);
      setEditorContent(notes[0].content);
    } else {
      setSelectedNote(null);
      setEditorContent("");
    }
  }

  // ─── 5) Submit new note (only if newContent is not blank) ─────────────────
  async function handleSubmitNew() {
    if (newContent.trim() === "") {
      toast.error("Cannot create an empty note.");
      return;
    }
    setIsSaving(true);
    try {
      const response = await api.post<Note>("/notes/", { content: newContent });
      const created = response.data;
      setNotes((prev) => [created, ...prev]);
      setSelectedNote(created);
      setEditorContent(created.content);
      setIsCreatingNew(false);
      setNewContent("");
      toast.success("Note created.");
    } catch (err) {
      toast.error("Failed to create note.");
    } finally {
      setIsSaving(false);
    }
  }

  // ─── 6) Save changes to the currently selected note ────────────────────────
  async function handleSaveNote() {
    if (!selectedNote) return;
    if (editorContent.trim() === "") {
      toast.error("Cannot save an empty note. Delete instead or add content.");
      return;
    }
    setIsSaving(true);
    try {
      const response = await api.put<Note>(`/notes/${selectedNote.id}/`, {
        content: editorContent,
      });
      const updated = response.data;
      setNotes((prev) => prev.map((n) => (n.id === updated.id ? updated : n)));
      setSelectedNote(updated);
      toast.success("Saved.");
    } catch (err) {
      toast.error("Failed to save note.");
    } finally {
      setIsSaving(false);
    }
  }

  // ─── 7) Delete the currently selected note ─────────────────────────────────
  async function handleDeleteNote() {
    if (!selectedNote) return;
    const idToDelete = selectedNote.id;
    try {
      await api.delete(`/notes/${idToDelete}/`);
      toast.success("Deleted.");
      const remaining = notes.filter((n) => n.id !== idToDelete);
      setNotes(remaining);
      if (remaining.length > 0) {
        setSelectedNote(remaining[0]);
        setEditorContent(remaining[0].content);
      } else {
        setSelectedNote(null);
        setEditorContent("");
      }
    } catch (err) {
      toast.error("Failed to delete note.");
    }
  }

  // ─── 8) Switch selection when user clicks a note in the sidebar ──────────
  function handleSelectNote(note: Note) {
    setIsCreatingNew(false);
    setSelectedNote(note);
    setEditorContent(note.content);
  }

  // ─── 9) Resizable Sidebar Logic ────────────────────────────────────────────
  const sidebarRef = useRef<HTMLDivElement>(null);
  const [sidebarWidth, setSidebarWidth] = useState<number>(250); // initial px
  const isResizingRef = useRef<boolean>(false);

  function onMouseDownDivider(e: React.MouseEvent) {
    isResizingRef.current = true;
  }

  function onMouseMove(e: MouseEvent) {
    if (!isResizingRef.current || !sidebarRef.current) return;
    // Calculate new width: distance from left of window to mouse X
    const newWidth = e.clientX;
    if (newWidth > 150 && newWidth < 600) {
      // clamp between 150px and 600px
      setSidebarWidth(newWidth);
    }
  }

  function onMouseUp() {
    isResizingRef.current = false;
  }

  useEffect(() => {
    // Attach document‐level listeners when resizing
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
    return () => {
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
    };
  }, []);

  // ─── Render ──────────────────────────────────────────────────────────────────
  return (
    <div className="h-screen flex overflow-hidden">
      {/* ───────────────────────────── Sidebar + Divider ───────────────────────────── */}
      <div
        ref={sidebarRef}
        style={{ width: sidebarWidth }}
        className="flex-shrink-0 border-r border-gray-200 dark:border-gray-700 flex flex-col"
      >
        <div className="px-4 py-3 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold">Your Notes</h2>
          <Button
            size="icon"
            variant="outline"
            onClick={handleStartNew}
            disabled={isSaving || isCreatingNew}
          >
            +<span className="sr-only">New note</span>
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
                        selectedNote?.id === note.id && !isCreatingNew
                          ? "bg-gray-200 dark:bg-gray-700"
                          : "hover:bg-gray-100 dark:hover:bg-gray-800"
                      }`}
                  >
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
      </div>

      {/* Drag‐handle / Divider between sidebar and main area */}
      <div
        onMouseDown={onMouseDownDivider}
        className="w-1 cursor-col-resize bg-transparent hover:bg-gray-300 dark:hover:bg-gray-600"
      />

      {/* ───────────────────────────── Main Editor Area ───────────────────────────── */}
      <div className="flex-1 flex flex-col">
        {/* Header with ModeToggle + Logout */}
        <header className="px-6 py-4 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
          <ModeToggle />
          <Button variant="ghost" size="sm" onClick={logout}>
            Log out
          </Button>
        </header>

        {/* ─── If we’re creating a new note ──────────────────────────────────────── */}
        {isCreatingNew ? (
          <div className="flex-1 p-6 flex flex-col">
            <Textarea
              className="flex-1 resize-none rounded-md border border-gray-300 dark:border-gray-600 p-4 focus:ring-2 focus:ring-indigo-500 focus:outline-none dark:bg-gray-800 dark:text-gray-100"
              placeholder="Type your new note here..."
              value={newContent}
              onChange={(e) => setNewContent(e.target.value)}
            />
            <div className="mt-4 flex justify-end space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handleCancelNew}
                disabled={isSaving}
              >
                Cancel
              </Button>
              <Button
                size="sm"
                onClick={handleSubmitNew}
                disabled={isSaving}
              >
                {isSaving ? "Saving…" : "Submit"}
              </Button>
            </div>
          </div>
        ) : !selectedNote ? (
          // ─── If no note is selected (and not creating one), show placeholder
          <div className="flex-1 flex items-center justify-center">
            <p className="text-gray-500 dark:text-gray-400">
              Select a note or click “+” to create one.
            </p>
          </div>
        ) : (
          // ─── Otherwise, editing an existing note ──────────────────────────────
          <div className="flex-1 p-6 flex flex-col">
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
