// src/pages/NotesPage.tsx

import { useEffect, useState } from "react";
import api from "@/api/api"; // Axios instance with JWT interceptor
import { useAuth } from "../context/AuthContext";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ModeToggle } from "@/components/mode-toggle";
import { toast } from "react-hot-toast";

import {
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle,
} from "@/components/ui/resizable";

import {
  SidebarProvider,
  SidebarTrigger,
  SidebarInset,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { Plus as PlusIcon } from "lucide-react";

interface Note {
  id: number;
  content: string;
  created_at: string;
  updated_at: string;
}

export default function NotesPage() {
  const { logout } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);

  // Always start with “create new” mode and an empty textarea
  const [isCreatingNew, setIsCreatingNew] = useState<boolean>(true);
  const [editorContent, setEditorContent] = useState<string>("");

  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isLoadingNotes, setIsLoadingNotes] = useState<boolean>(true);

  // ─── Fetch all notes on mount ───────────────────────────────────────────────
  useEffect(() => {
    async function fetchNotes() {
      setIsLoadingNotes(true);
      try {
        const response = await api.get<Note[]>("/notes/");
        setNotes(response.data);
        // Do NOT auto-select any note; remain in “create new” mode with empty textarea
      } catch {
        toast.error("Failed to load notes.");
      } finally {
        setIsLoadingNotes(false);
      }
    }
    fetchNotes();
  }, []);

  // ─── Handler for clicking “+” (start new note) ─────────────────────────────
  function handleStartNew() {
    setIsCreatingNew(true);
    setSelectedNote(null);
    setEditorContent(""); // ensure textarea is empty
  }

  // ─── Submit new note ────────────────────────────────────────────────────────
  async function handleSubmitNew() {
    if (editorContent.trim() === "") {
      toast.error("Cannot create an empty note.");
      return;
    }
    setIsSaving(true);
    try {
      const response = await api.post<Note>("/notes/", { content: editorContent });
      const created = response.data;
      setNotes((prev) => [created, ...prev]);
      toast.success("Note created.");
      // After creating, clear textarea and stay in “create new” mode
      setEditorContent("");
      setIsCreatingNew(true);
      setSelectedNote(null);
    } catch {
      toast.error("Failed to create note.");
    } finally {
      setIsSaving(false);
    }
  }

  // ─── Select note from sidebar ───────────────────────────────────────────────
  function handleSelectNote(note: Note) {
    setIsCreatingNew(false);
    setSelectedNote(note);
    setEditorContent(note.content);
  }

  // ─── Save existing note ─────────────────────────────────────────────────────
  async function handleSaveNote() {
    if (!selectedNote) return;
    if (editorContent.trim() === "") {
      toast.error("Cannot save an empty note.");
      return;
    }
    setIsSaving(true);
    try {
      const response = await api.put<Note>(`/notes/${selectedNote.id}/`, {
        content: editorContent,
      });
      const updated = response.data;
      setNotes((prev) => prev.map((n) => (n.id === updated.id ? updated : n)));
      toast.success("Saved.");
      setEditorContent(updated.content);
    } catch {
      toast.error("Failed to save note.");
    } finally {
      setIsSaving(false);
    }
  }

  // ─── Delete existing note ───────────────────────────────────────────────────
  async function handleDeleteNote() {
    if (!selectedNote) return;
    const idToDelete = selectedNote.id;
    try {
      await api.delete(`/notes/${idToDelete}/`);
      toast.success("Deleted.");
      const remaining = notes.filter((n) => n.id !== idToDelete);
      setNotes(remaining);
      // After deletion, go back to “create new” mode with empty textarea
      setSelectedNote(null);
      setEditorContent("");
      setIsCreatingNew(true);
    } catch {
      toast.error("Failed to delete note.");
    }
  }

  // ─── Render ──────────────────────────────────────────────────────────────────
  return (
    <SidebarProvider>
      <AppSidebar />

      <SidebarInset className="h-screen">
        <div className="flex h-full flex-col">
          {/* Header with SidebarTrigger + ModeToggle + Logout */}
          <header className="flex h-16 items-center justify-between border-b border-gray-200 dark:border-gray-700 px-6">
            <div className="flex items-center space-x-2">
              <SidebarTrigger />
              <ModeToggle />
            </div>
            <Button variant="ghost" size="sm" onClick={logout}>
              Log out
            </Button>
          </header>

          {/* Resizable Panels: Sidebar vs. Main Editor */}
          <div className="flex flex-1 overflow-hidden">
            <ResizablePanelGroup direction="horizontal" className="flex-1">
              {/* ─── Sidebar Panel ─────────────────────────────────────────────── */}
              <ResizablePanel defaultSize={25} minSize={15} className="border-r border-gray-200 dark:border-gray-700 flex flex-col">
                <div className="px-4 py-3 flex items-center justify-between border-b border-gray-200 dark:border-gray-700">
                  <h2 className="text-lg font-semibold">Your Notes</h2>
                  <Button
                    size="icon"
                    variant="outline"
                    onClick={handleStartNew}
                    disabled={isSaving}
                  >
                    <PlusIcon className="h-5 w-5" />
                    <span className="sr-only">New note</span>
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
              </ResizablePanel>

              <ResizableHandle withHandle />

              {/* ─── Main Editor Panel ──────────────────────────────────────────── */}
              <ResizablePanel defaultSize={75} className="flex flex-col">
                {isCreatingNew ? (
                  // ─── Always-empty textarea for “create new” mode ───────────────
                  <div className="flex h-full flex-col p-6">
                    <Textarea
                      className="min-h-[200px] flex-1 resize-none rounded-md border border-gray-300 dark:border-gray-600 p-4 focus:ring-2 focus:ring-indigo-500 focus:outline-none dark:bg-gray-800 dark:text-gray-100"
                      placeholder="Type your new note here..."
                      value={editorContent}        // bound to editorContent (always "")
                      onChange={(e) => setEditorContent(e.target.value)}
                    />
                    <div className="mt-4 flex justify-end space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setEditorContent("");
                          setIsCreatingNew(false);
                        }}
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
                  // ─── Placeholder when not creating and no note selected ───
                  <div className="flex h-full items-center justify-center">
                    <p className="text-gray-500 dark:text-gray-400">
                      Select a note or click “+” to create one.
                    </p>
                  </div>
                ) : (
                  // ─── Edit existing note ───────────────────────────────────
                  <div className="flex h-full flex-col p-6">
                    <Textarea
                      className="min-h-[200px] flex-1 resize-none rounded-md border border-gray-300 dark:border-gray-600 p-4 focus:ring-2 focus:ring-indigo-500 focus:outline-none dark:bg-gray-800 dark:text-gray-100"
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
              </ResizablePanel>
            </ResizablePanelGroup>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
