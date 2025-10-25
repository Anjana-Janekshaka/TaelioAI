"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Sparkles, ArrowLeft, Zap, Crown, Star } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

interface Tier {
  id: string;
  name: string;
  price: string;
  description: string;
  features: string[];
  popular?: boolean;
  icon: any;
  color: string;
  gradient: string;
}

export default function SelectTierPage() {
  const [selectedTier, setSelectedTier] = useState<string>("free");
  const router = useRouter();

  const tiers: Tier[] = [
    {
      id: "free",
      name: "Free",
      price: "$0",
      description: "Perfect for getting started",
      features: [
        "2 requests per minute",
        "Basic AI assistance",
        "Standard genres",
        "Community support",
        "Basic rate limits"
      ],
      icon: Sparkles,
      color: "from-gray-500 to-gray-600",
      gradient: "from-gray-50 to-gray-100"
    },
    {
      id: "pro",
      name: "Pro",
      price: "$19",
      description: "For serious writers",
      features: [
        "10 requests per minute",
        "Advanced AI assistance",
        "All genres & tones",
        "Priority support",
        "Higher rate limits",
        "Better model access",
        "Enhanced features"
      ],
      popular: true,
      icon: Zap,
      color: "from-blue-500 to-blue-600",
      gradient: "from-blue-50 to-blue-100"
    }
  ];

  const handleContinue = () => {
    // TODO: Save selected tier and continue to registration
    router.push(`/register?tier=${selectedTier}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Back to Home */}
        <Link href="/" className="inline-flex items-center text-gray-600 hover:text-blue-600 mb-8">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Home
        </Link>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl mb-6">
            <Star className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Select the perfect tier for your storytelling journey. You can always upgrade or downgrade later.
          </p>
        </motion.div>

        {/* Tier Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12 max-w-4xl mx-auto">
          {tiers.map((tier, index) => (
            <motion.div
              key={tier.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              className={`relative bg-white rounded-2xl shadow-lg border-2 transition-all duration-300 ${
                selectedTier === tier.id
                  ? "border-blue-500 shadow-xl"
                  : "border-gray-200 hover:border-gray-300"
              } ${tier.popular ? "ring-2 ring-blue-500 ring-opacity-50" : ""}`}
            >
              {tier.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-2 rounded-full text-sm font-semibold">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="p-8">
                {/* Tier Header */}
                <div className="text-center mb-6">
                  <motion.div
                    className={`w-16 h-16 mx-auto mb-4 bg-gradient-to-r ${tier.color} rounded-2xl flex items-center justify-center`}
                    whileHover={{ rotate: 5, scale: 1.1 }}
                    transition={{ duration: 0.2 }}
                  >
                    <tier.icon className="h-8 w-8 text-white" />
                  </motion.div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{tier.name}</h3>
                  <div className="text-4xl font-bold text-gray-900 mb-2">{tier.price}</div>
                  <p className="text-gray-600">{tier.description}</p>
                </div>

                {/* Features */}
                <div className="space-y-4 mb-8">
                  {tier.features.map((feature, featureIndex) => (
                    <motion.div
                      key={featureIndex}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.4, delay: 0.1 + featureIndex * 0.05 }}
                      className="flex items-center space-x-3"
                    >
                      <div className="flex-shrink-0">
                        <Check className="h-5 w-5 text-green-500" />
                      </div>
                      <span className="text-gray-700">{feature}</span>
                    </motion.div>
                  ))}
                </div>

                {/* Select Button */}
                <motion.button
                  onClick={() => setSelectedTier(tier.id)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full py-3 rounded-xl font-semibold transition-all ${
                    selectedTier === tier.id
                      ? `bg-gradient-to-r ${tier.color} text-white shadow-lg`
                      : `bg-gradient-to-r ${tier.gradient} text-gray-700 border border-gray-300 hover:border-gray-400`
                  }`}
                >
                  {selectedTier === tier.id ? "Selected" : "Select Plan"}
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Continue Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center"
        >
          <motion.button
            onClick={handleContinue}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
          >
            Continue with {tiers.find(t => t.id === selectedTier)?.name} Plan
          </motion.button>
          
          <p className="text-sm text-gray-500 mt-4">
            You can change your plan anytime in your account settings
          </p>
        </motion.div>

        {/* FAQ Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6 }}
          className="mt-16 bg-white rounded-2xl shadow-lg p-8"
        >
          <h3 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            Frequently Asked Questions
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Can I change my plan later?</h4>
              <p className="text-gray-600 text-sm">Yes! You can upgrade or downgrade your plan at any time from your account settings.</p>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">What happens to my stories?</h4>
              <p className="text-gray-600 text-sm">All your stories are saved and accessible regardless of your plan level.</p>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Is there a free trial?</h4>
              <p className="text-gray-600 text-sm">Yes! Start with our free plan and upgrade when you're ready for more features.</p>
            </div>
            
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">What payment methods do you accept?</h4>
              <p className="text-gray-600 text-sm">We accept all major credit cards, PayPal, and bank transfers.</p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}