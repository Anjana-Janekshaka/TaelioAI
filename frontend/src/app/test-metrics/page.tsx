"use client";

import { useState } from "react";
import UserMetricsDropdown from "@/components/UserMetricsDropdown";

export default function TestMetricsPage() {
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Test Metrics Dropdown</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">User Metrics Dropdown Test</h2>
          
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Toggle Metrics Dropdown
          </button>
          
          <div className="mt-4 relative">
            <UserMetricsDropdown 
              isOpen={showDropdown} 
              onClose={() => setShowDropdown(false)} 
            />
          </div>
        </div>
      </div>
    </div>
  );
}
