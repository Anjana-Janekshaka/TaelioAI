import React from 'react'

const StoryDisplay = ({ story, onNewStory }) => {
    if (!story) return null

    return (
        <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-3xl font-bold text-gray-900">Generated Story</h2>
                <button
                    onClick={onNewStory}
                    className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
                >
                    Write Another Story
                </button>
            </div>
            
            <div className="prose prose-lg max-w-none">
                <div className="bg-gray-50 p-6 rounded-lg border-l-4 border-indigo-500">
                    <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                        {story}
                    </div>
                </div>
            </div>
            
            {/* Action Buttons */}
            <div className="mt-6 flex flex-wrap gap-3">
                <button
                    onClick={() => {
                        navigator.clipboard.writeText(story)
                        // You could add a toast notification here
                    }}
                    className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors flex items-center"
                >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    Copy Story
                </button>
                
                <button
                    onClick={() => {
                        const blob = new Blob([story], { type: 'text/plain' })
                        const url = URL.createObjectURL(blob)
                        const a = document.createElement('a')
                        a.href = url
                        a.download = 'my-story.txt'
                        document.body.appendChild(a)
                        a.click()
                        document.body.removeChild(a)
                        URL.revokeObjectURL(url)
                    }}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center"
                >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Download Story
                </button>
                
                <button
                    onClick={() => {
                        const printWindow = window.open('', '_blank')
                        printWindow.document.write(`
                            <html>
                                <head>
                                    <title>My Story</title>
                                    <style>
                                        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }
                                        h1 { color: #4f46e5; }
                                    </style>
                                </head>
                                <body>
                                    <h1>My Story</h1>
                                    <div style="white-space: pre-wrap;">${story}</div>
                                </body>
                            </html>
                        `)
                        printWindow.document.close()
                        printWindow.print()
                    }}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                    </svg>
                    Print Story
                </button>
            </div>
        </div>
    )
}

export default StoryDisplay

