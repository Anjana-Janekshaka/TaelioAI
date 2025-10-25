"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, BookOpen, PenTool, Brain, Zap, Star } from "lucide-react";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import IdeaGenerator from "@/components/IdeaGenerator";
import StoryWriter from "@/components/StoryWriter";
import WorkflowSelector from "@/components/WorkflowSelector";
import Features from "@/components/Features";
import Footer from "@/components/Footer";

export default function Home() {
  const [activeTab, setActiveTab] = useState("idea");

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <Hero />
        
        <motion.div
          id="workflow"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-16"
        >
          <WorkflowSelector activeTab={activeTab} setActiveTab={setActiveTab} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-8"
        >
          {activeTab === "idea" && <IdeaGenerator />}
          {activeTab === "story" && <StoryWriter />}
          {activeTab === "workflow" && <div>Full Workflow Coming Soon...</div>}
        </motion.div>

        <Features />
      </main>

      <Footer />
    </div>
  );
}