"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { PenTool, BookOpen, Copy, Download, RefreshCw, Save, AlertCircle } from "lucide-react";
import { useStoryWriting } from "@/hooks/useApi";

export default function StoryWriter() {
  const [title, setTitle] = useState("");
  const [genre, setGenre] = useState("Fantasy");
  const [tone, setTone] = useState("Adventurous");
  const [outline, setOutline] = useState("");
  const [characters, setCharacters] = useState("");
  const [setting, setSetting] = useState("");
  const { story, loading, error, writeStory, reset } = useStoryWriting();

  const genres = ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Thriller", "Adventure", "Drama"];
  const tones = ["Adventurous", "Dark", "Light-hearted", "Mysterious", "Romantic", "Gritty", "Whimsical", "Dramatic"];

  const handleGenerate = async () => {
    if (!title.trim()) return;
    
    try {
      await writeStory({
        title,
        genre,
        tone,
        outline,
        characters,
        setting
      });
    } catch (error) {
      console.error('Error writing story:', error);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const downloadStory = () => {
    if (!story || !story.story) return;
    
    const element = document.createElement('a');
    const file = new Blob([story.story], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `${(title || 'story').replace(/\s+/g, '_')}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 bg-purple-50 text-purple-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
          <PenTool className="h-4 w-4" />
          <span>Story Writer</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Write Complete Stories</h2>
        <p className="text-gray-600">Transform your ideas into compelling narratives</p>
      </div>

      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Story Title *
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter your story title..."
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Genre
                </label>
                <select
                  value={genre}
                  onChange={(e) => setGenre(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  {genres.map((g) => (
                    <option key={g} value={g}>{g}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tone
                </label>
                <select
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                >
                  {tones.map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Story Outline (Optional)
              </label>
              <textarea
                value={outline}
                onChange={(e) => setOutline(e.target.value)}
                placeholder="Brief outline of your story..."
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                rows={3}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Characters (Optional)
              </label>
              <textarea
                value={characters}
                onChange={(e) => setCharacters(e.target.value)}
                placeholder="Describe your main characters..."
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                rows={2}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Setting (Optional)
              </label>
              <textarea
                value={setting}
                onChange={(e) => setSetting(e.target.value)}
                placeholder="Describe the world or setting..."
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                rows={2}
              />
            </div>

            <motion.button
              onClick={handleGenerate}
              disabled={!title.trim() || loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <RefreshCw className="h-5 w-5 animate-spin" />
                  <span>Writing Story...</span>
                </>
              ) : (
                <>
                  <BookOpen className="h-5 w-5" />
                  <span>Write Story</span>
                </>
              )}
            </motion.button>
          </div>

          {/* Results */}
          <div className="space-y-6">
            {error && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-50 border border-red-200 rounded-xl p-4"
              >
                <div className="flex items-center space-x-2 text-red-700">
                  <AlertCircle className="h-4 w-4" />
                  <span className="font-medium">Error writing story</span>
                </div>
                <p className="text-red-600 text-sm mt-1">{error}</p>
              </motion.div>
            )}

                        {story ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-6 rounded-xl">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-gray-900">{title || "Untitled Story"}</h3>
                    <div className="flex items-center space-x-2">
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                        {genre || "Unknown Genre"}
                      </span>
                      <span className="px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-sm">
                        {tone || "Unknown Tone"}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span>{(story.story || "").split(/\s+/).length} words</span>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => copyToClipboard(story.story || "")}
                        className="p-2 hover:bg-white/50 rounded-lg transition-colors"
                        title="Copy story"
                      >
                        <Copy className="h-4 w-4" />
                      </button>
                      <button
                        onClick={downloadStory}
                        className="p-2 hover:bg-white/50 rounded-lg transition-colors"
                        title="Download story"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                      <button
                        className="p-2 hover:bg-white/50 rounded-lg transition-colors"
                        title="Save story"
                      >
                        <Save className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="bg-white border border-gray-200 rounded-xl p-8 max-h-[500px] overflow-y-auto shadow-sm">
                  <div className="prose prose-lg max-w-none prose-headings:text-gray-900 prose-h1:text-3xl prose-h2:text-2xl prose-h3:text-xl prose-h2:font-bold prose-h3:font-semibold prose-p:text-gray-700 prose-p:leading-relaxed prose-p:mb-4 prose-strong:text-gray-900 prose-em:text-gray-600">
                    <div className="whitespace-pre-wrap text-gray-800 font-serif leading-7" 
                         style={{ 
                           fontFamily: 'Georgia, serif',
                           fontSize: '1.125rem',
                           lineHeight: '1.875rem'
                         }}
                         dangerouslySetInnerHTML={{ __html: (story.story || "No content available").replace(/\n/g, '<br/>') }} 
                    />
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Your generated story will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
