"use client";

import { motion } from "framer-motion";
import { Brain, PenTool, Workflow, Zap, Shield, Sparkles, Users, BookOpen } from "lucide-react";

export default function Features() {
  const features = [
    {
      icon: Brain,
      title: "AI-Powered Idea Generation",
      description: "Generate creative story concepts from simple prompts using advanced AI technology",
      color: "from-blue-500 to-blue-600"
    },
    {
      icon: PenTool,
      title: "Intelligent Story Writing",
      description: "Transform your ideas into compelling narratives with AI assistance",
      color: "from-purple-500 to-purple-600"
    },
    {
      icon: Workflow,
      title: "Complete Workflow",
      description: "End-to-end story creation from concept to final draft",
      color: "from-green-500 to-green-600"
    },
    {
      icon: Zap,
      title: "Lightning Fast",
      description: "Generate stories and ideas in seconds, not hours",
      color: "from-yellow-500 to-orange-500"
    },
    {
      icon: Shield,
      title: "Quality Assurance",
      description: "Built-in quality checks ensure your stories are polished and engaging",
      color: "from-red-500 to-pink-500"
    },
    {
      icon: Sparkles,
      title: "Creative Enhancement",
      description: "AI agents work together to enhance creativity and storytelling",
      color: "from-pink-500 to-purple-500"
    }
  ];

  const stats = [
    { label: "Stories Generated", value: "10,000+", icon: BookOpen },
    { label: "Happy Writers", value: "5,000+", icon: Users },
    { label: "AI Agents", value: "4", icon: Brain },
    { label: "Success Rate", value: "99.9%", icon: Zap }
  ];

  return (
    <section id="features" className="py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Powerful Features for Creative Writers
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover the tools and capabilities that make TaelioAI the perfect companion for your creative journey
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              className="bg-white rounded-2xl p-8 shadow-lg border border-gray-100 hover:shadow-xl transition-all"
            >
              <motion.div
                className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-2xl flex items-center justify-center mb-6`}
                whileHover={{ rotate: 5, scale: 1.1 }}
                transition={{ duration: 0.2 }}
              >
                <feature.icon className="h-8 w-8 text-white" />
              </motion.div>
              
              <h3 className="text-xl font-bold text-gray-900 mb-4">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Stats Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl p-12 text-white"
        >
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Trusted by Writers Worldwide</h2>
            <p className="text-blue-100 text-lg">
              Join thousands of creators who are already using TaelioAI
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="text-center"
              >
                <motion.div
                  className="w-16 h-16 bg-white/20 rounded-2xl flex items-center justify-center mx-auto mb-4"
                  whileHover={{ scale: 1.1 }}
                >
                  <stat.icon className="h-8 w-8" />
                </motion.div>
                <div className="text-3xl font-bold mb-2">{stat.value}</div>
                <div className="text-blue-100">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* CTA Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mt-20"
        >
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Ready to Start Creating?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of writers who are already using TaelioAI to bring their stories to life
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
          >
            Get Started Now
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
}
