"use client";

import { motion } from "framer-motion";
import { Shield, BarChart3, TrendingUp, AlertTriangle } from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ModerationMetrics from "@/components/ModerationMetrics";

export default function MetricsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {/* Page Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <div className="flex items-center justify-center mb-4">
            <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
              <Shield className="h-8 w-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Content Moderation Metrics
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Track and analyze content moderation performance, safety scores, and violation patterns 
            to ensure high-quality, safe content generation.
          </p>
        </motion.div>

        {/* Metrics Overview Cards */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8"
        >
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-blue-100 rounded-lg">
                <BarChart3 className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800">Analytics</h3>
            </div>
            <p className="text-gray-600">
              Comprehensive metrics on content moderation performance, including safety scores, 
              violation detection, and content quality assessment.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-green-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800">Performance</h3>
            </div>
            <p className="text-gray-600">
              Track improvements in content safety over time and identify patterns in 
              content moderation effectiveness.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-red-100 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-800">Safety</h3>
            </div>
            <p className="text-gray-600">
              Monitor violation detection rates, unsafe content identification, and 
              overall content safety metrics.
            </p>
          </div>
        </motion.div>

        {/* Main Metrics Component */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <ModerationMetrics />
        </motion.div>

        {/* Additional Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-12 bg-white rounded-lg shadow-md p-6"
        >
          <h2 className="text-2xl font-bold text-gray-800 mb-4">About Content Moderation</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">How It Works</h3>
              <p className="text-gray-600">
                Our AI-powered content moderation system automatically analyzes all generated content 
                for safety, appropriateness, and policy compliance. It checks for inappropriate keywords, 
                safety patterns, and content quality issues.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Safety Scores</h3>
              <p className="text-gray-600">
                Content is scored on a scale of 0-100, with higher scores indicating safer content. 
                Scores below 70 may require review, while scores below 50 are flagged as potentially unsafe.
              </p>
            </div>
          </div>
        </motion.div>
      </main>

      <Footer />
    </div>
  );
}
