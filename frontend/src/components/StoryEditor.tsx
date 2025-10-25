"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Edit3, Save, RotateCcw, Eye, Download } from "lucide-react";
import { apiService, StoryEditRequest } from "@/lib/api";

interface StoryEditorProps {
  story?: string;
  title?: string;
  genre?: string;
}

export default function StoryEditor({ story, title, genre }: StoryEditorProps) {
  const [editedStory, setEditedStory] = useState(story || "");
  const [editInstructions, setEditInstructions] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  const handleEdit = async () => {
    if (!editInstructions.trim()) {
      alert("Please provide edit instructions");
      return;
    }

    setIsLoading(true);
    try {
      const request: StoryEditRequest = {
        story: editedStory,
        edit_instructions: editInstructions,
        title: title || "Edited Story",
        genre: genre || "General"
      };

      const response = await apiService.editStory(request);
      
      if (response.success) {
        setEditedStory(response.edited_story);
        setIsEditing(false);
        setEditInstructions("");
        alert("Story edited successfully!");
      } else {
        alert("Failed to edit story");
      }
    } catch (error) {
      console.error("Error editing story:", error);
      alert("Error editing story. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = () => {
    // TODO: Implement save functionality
    console.log("Saving story:", editedStory);
    alert("Story saved successfully!");
  };

  const handleReset = () => {
    setEditedStory(story || "");
    setEditInstructions("");
    setIsEditing(false);
  };

  const handleDownload = () => {
    const element = document.createElement("a");
    const file = new Blob([editedStory], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = `${title || "story"}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  if (!story) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8 text-center">
        <div className="text-gray-500 mb-4">
          <Edit3 className="w-16 h-16 mx-auto mb-4 text-gray-300" />
        </div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">
          Full Workflow Coming Soon...
        </h3>
        <p className="text-gray-500">
          Generate a story first to access the story editor
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
            <Edit3 className="w-6 h-6" />
            Story Editor
          </h2>
          {title && (
            <p className="text-gray-600 mt-1">
              {title} {genre && `• ${genre}`}
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <Eye className="w-4 h-4" />
            {showPreview ? "Edit" : "Preview"}
          </button>
          <button
            onClick={handleDownload}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <Download className="w-4 h-4" />
            Download
          </button>
        </div>
      </div>

      {!showPreview ? (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Edit Instructions
            </label>
            <textarea
              value={editInstructions}
              onChange={(e) => setEditInstructions(e.target.value)}
              placeholder="Describe what changes you'd like to make to the story..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={3}
            />
          </div>

          <div className="flex gap-3">
            <button
              onClick={handleEdit}
              disabled={isLoading || !editInstructions.trim()}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <Edit3 className="w-4 h-4" />
              )}
              {isLoading ? "Editing..." : "Apply Edit"}
            </button>
            <button
              onClick={handleReset}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              Reset
            </button>
            <button
              onClick={handleSave}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Save className="w-4 h-4" />
              Save
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Story Content
            </label>
            <textarea
              value={editedStory}
              onChange={(e) => setEditedStory(e.target.value)}
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={15}
              placeholder="Your story will appear here..."
            />
          </div>
        </div>
      ) : (
        <div className="prose max-w-none">
          <div className="bg-gray-50 p-6 rounded-lg">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Story Preview
            </h3>
            <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
              {editedStory}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
