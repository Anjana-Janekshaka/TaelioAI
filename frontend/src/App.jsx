import React, { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import StoryWriterForm from './components/StoryWriterForm'
import StoryDisplay from './components/StoryDisplay'

function App() {
  const [generatedStory, setGeneratedStory] = useState(null)

  const handleStoryGenerated = (storyData) => {
    setGeneratedStory(storyData.story)
  }

  const handleNewStory = () => {
    setGeneratedStory(null)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      
      <main className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
              Welcome to <span className="text-indigo-600">TaelioAI</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              Create amazing stories with the power of AI. Simply provide a title, genre, and outline, and watch your story come to life.
            </p>
          </div>

          {/* Story Writing Section */}
          {!generatedStory ? (
            <StoryWriterForm onStoryGenerated={handleStoryGenerated} />
          ) : (
            <StoryDisplay story={generatedStory} onNewStory={handleNewStory} />
          )}

          {/* Features Section */}
          <div className="mt-20">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900">Why Choose TaelioAI?</h2>
              <p className="mt-4 text-lg text-gray-600">Powerful AI-driven story generation</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-indigo-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">AI-Powered</h3>
                <p className="text-gray-600">Advanced AI technology creates engaging and creative stories tailored to your preferences.</p>
              </div>
              
              <div className="text-center">
                <div className="bg-indigo-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Fast Generation</h3>
                <p className="text-gray-600">Get your complete story in seconds, not hours. Perfect for writers, students, and creative minds.</p>
              </div>
              
              <div className="text-center">
                <div className="bg-indigo-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">Multiple Genres</h3>
                <p className="text-gray-600">Choose from various genres including Fantasy, Sci-Fi, Mystery, Romance, and many more.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
