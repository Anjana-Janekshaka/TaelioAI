"use client";

import { motion } from "framer-motion";
import { Sparkles, BookOpen, PenTool, Brain, ArrowRight } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";

export default function Hero() {
  const { user, isAuthenticated } = useAuth();
  
  return (
    <section className="text-center py-16 md:py-24">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="max-w-4xl mx-auto"
      >
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="inline-flex items-center space-x-2 bg-blue-50 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-8"
        >
          <Sparkles className="h-4 w-4" />
          <span>AI-Powered Story Generation</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="text-5xl md:text-7xl font-bold mb-6"
        >
          {isAuthenticated ? (
            <>
              <span className="gradient-text">Welcome back, {user?.email?.split('@')[0]}!</span>
              <br />
              <span className="text-gray-900">Ready to create stories?</span>
            </>
          ) : (
            <>
              <span className="gradient-text">Your AI</span>
              <br />
              <span className="text-gray-900">Storytelling Companion</span>
            </>
          )}
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed"
        >
          {isAuthenticated ? (
            `Start generating creative story ideas and writing compelling narratives with your ${user?.role === 'pro' ? 'Pro' : 'Free'} plan. Let's bring your stories to life!`
          ) : (
            "Generate creative story ideas, write compelling narratives, and bring your stories to life with the power of AI. Perfect for writers, creators, and storytellers."
          )}
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.7 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          {isAuthenticated ? (
            <>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center space-x-2"
                onClick={() => document.getElementById('workflow')?.scrollIntoView({ behavior: 'smooth' })}
              >
                <span>Start Creating Stories</span>
                <ArrowRight className="h-5 w-5" />
              </motion.button>
              
              {user?.role === 'free' && (
                <motion.a
                  href="/select-tier"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 border-2 border-yellow-500 text-yellow-600 rounded-xl font-semibold text-lg hover:border-yellow-600 hover:text-yellow-700 transition-all"
                >
                  Upgrade to Pro
                </motion.a>
              )}
            </>
          ) : (
            <>
              <motion.a
                href="/select-tier"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all flex items-center space-x-2"
              >
                <span>Start Creating</span>
                <ArrowRight className="h-5 w-5" />
              </motion.a>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold text-lg hover:border-blue-500 hover:text-blue-600 transition-all"
              >
                Learn More
              </motion.button>
            </>
          )}
        </motion.div>
      </motion.div>

      {/* Feature Icons */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.9 }}
        className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
      >
        {[
          { icon: Brain, label: "Idea Generation", color: "from-blue-500 to-blue-600" },
          { icon: PenTool, label: "Story Writing", color: "from-purple-500 to-purple-600" },
          { icon: BookOpen, label: "Full Workflow", color: "from-green-500 to-green-600" },
          { icon: Sparkles, label: "AI Enhancement", color: "from-pink-500 to-pink-600" },
        ].map((feature, index) => (
          <motion.div
            key={feature.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1 + index * 0.1 }}
            className="text-center"
          >
            <motion.div
              whileHover={{ scale: 1.1, rotate: 5 }}
              className={`w-16 h-16 mx-auto mb-4 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center shadow-lg`}
            >
              <feature.icon className="h-8 w-8 text-white" />
            </motion.div>
            <p className="text-sm font-medium text-gray-700">{feature.label}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
