"use client";

import { motion } from "framer-motion";
import { Brain, PenTool, Workflow } from "lucide-react";

interface WorkflowSelectorProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export default function WorkflowSelector({ activeTab, setActiveTab }: WorkflowSelectorProps) {
  const tabs = [
    {
      id: "idea",
      label: "Idea Generator",
      icon: Brain,
      description: "Generate creative story ideas from simple prompts",
      color: "from-blue-500 to-blue-600"
    },
    {
      id: "story",
      label: "Story Writer",
      icon: PenTool,
      description: "Write complete stories from your ideas",
      color: "from-purple-500 to-purple-600"
    },
    {
      id: "workflow",
      label: "Full Workflow",
      icon: Workflow,
      description: "Complete end-to-end story generation",
      color: "from-green-500 to-green-600"
    }
  ];

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Choose Your Workflow</h2>
        <p className="text-gray-600">Select how you'd like to create your story</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {tabs.map((tab) => (
          <motion.button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`p-6 rounded-xl border-2 transition-all duration-300 ${
              activeTab === tab.id
                ? "border-blue-500 bg-blue-50 shadow-lg"
                : "border-gray-200 hover:border-gray-300 hover:shadow-md"
            }`}
          >
            <div className="text-center">
              <motion.div
                className={`w-12 h-12 mx-auto mb-4 bg-gradient-to-r ${tab.color} rounded-xl flex items-center justify-center ${
                  activeTab === tab.id ? "shadow-lg" : ""
                }`}
                animate={{ scale: activeTab === tab.id ? 1.1 : 1 }}
                transition={{ duration: 0.2 }}
              >
                <tab.icon className="h-6 w-6 text-white" />
              </motion.div>
              
              <h3 className={`text-lg font-semibold mb-2 ${
                activeTab === tab.id ? "text-blue-700" : "text-gray-900"
              }`}>
                {tab.label}
              </h3>
              
              <p className="text-sm text-gray-600 leading-relaxed">
                {tab.description}
              </p>
            </div>
          </motion.button>
        ))}
      </div>
    </div>
  );
}
