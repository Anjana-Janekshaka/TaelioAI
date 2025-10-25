"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Brain, Sparkles, Copy, RefreshCw, Lightbulb, AlertCircle } from "lucide-react";
import { useIdeaGeneration } from "@/hooks/useApi";

export default function IdeaGenerator() {
  const [prompt, setPrompt] = useState("");
  const [genre, setGenre] = useState("Fantasy");
  const [tone, setTone] = useState("Adventurous");
  const { idea, loading, error, generateIdea, reset } = useIdeaGeneration();

  const genres = ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", "Thriller", "Adventure", "Drama"];
  const tones = ["Adventurous", "Dark", "Light-hearted", "Mysterious", "Romantic", "Gritty", "Whimsical", "Dramatic"];

  const examplePrompts = [
    "A mysterious lighthouse keeper",
    "A time-traveling chef",
    "A magical library that changes every night",
    "A detective who can see memories"
  ];

  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    try {
      await generateIdea(prompt, genre, tone);
    } catch (error) {
      console.error('Error generating idea:', error);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
      <div className="text-center mb-8">
        <div className="inline-flex items-center space-x-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-4">
          <Brain className="h-4 w-4" />
          <span>Idea Generator</span>
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Generate Creative Story Ideas</h2>
        <p className="text-gray-600">Describe your concept and let AI create a detailed story idea</p>
      </div>

      <div className="max-w-4xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Story Prompt
              </label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your story concept... (e.g., 'A mysterious lighthouse keeper')"
                className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={4}
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
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
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
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {tones.map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Example Prompts
              </label>
              <div className="grid grid-cols-2 gap-2">
                {examplePrompts.map((example, index) => (
                  <button
                    key={index}
                    onClick={() => setPrompt(example)}
                    className="p-2 text-sm text-left bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>

            <motion.button
              onClick={handleGenerate}
              disabled={!prompt.trim() || loading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <RefreshCw className="h-5 w-5 animate-spin" />
                  <span>Generating...</span>
                </>
              ) : (
                <>
                  <Sparkles className="h-5 w-5" />
                  <span>Generate Idea</span>
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
                  <span className="font-medium">Error generating idea</span>
                </div>
                <p className="text-red-600 text-sm mt-1">{error}</p>
              </motion.div>
            )}

            {idea ? (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-xl">
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{idea.title || "Untitled Story"}</h3>
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm">
                      {idea.genre || "Unknown Genre"}
                    </span>
                    <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">
                      {idea.tone || "Unknown Tone"}
                    </span>
                  </div>
                  <p className="text-gray-700 leading-relaxed">{idea.outline || "No outline available"}</p>
                </div>

                <div className="grid grid-cols-1 gap-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2 flex items-center space-x-2">
                      <Lightbulb className="h-4 w-4" />
                      <span>Characters</span>
                    </h4>
                    <div className="space-y-1">
                      {idea.characters && idea.characters.length > 0 ? (
                        idea.characters.map((character, index) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                            <span className="text-sm text-gray-700">{character}</span>
                            <button
                              onClick={() => copyToClipboard(character)}
                              className="p-1 hover:bg-gray-200 rounded"
                            >
                              <Copy className="h-3 w-3" />
                            </button>
                          </div>
                        ))
                      ) : (
                        <div className="p-3 bg-gray-50 rounded-lg">
                          <p className="text-sm text-gray-500 italic">No characters generated</p>
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Setting</h4>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-700">{idea.setting || "No setting information available"}</p>
                    </div>
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Brain className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>Your generated story idea will appear here</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
