"use client";

import { motion } from "framer-motion";
import { Check, X, Zap, Crown, Star } from "lucide-react";

interface TierLimitsProps {
  currentTier: string;
  className?: string;
}

const tierData = {
  free: {
    name: "Free",
    icon: <Zap className="h-5 w-5 text-gray-500" />,
    color: "from-gray-500 to-gray-600",
    requestsPerDay: 50,
    requestsPerMinute: 2,
    tokensPerDay: 10000,
    features: [
      "Basic story generation",
      "Idea generation",
      "Limited API access",
      "Community support"
    ],
    limitations: [
      "No advanced features",
      "Rate limited"
    ]
  },
  pro: {
    name: "Pro",
    icon: <Star className="h-5 w-5 text-yellow-500" />,
    color: "from-yellow-500 to-orange-500",
    requestsPerDay: 500,
    requestsPerMinute: 10,
    tokensPerDay: 100000,
    features: [
      "All free features",
      "Advanced story templates",
      "Priority processing",
      "Email support",
      "API key management"
    ],
    limitations: []
  },
  admin: {
    name: "Admin",
    icon: <Crown className="h-5 w-5 text-purple-500" />,
    color: "from-purple-500 to-pink-500",
    requestsPerDay: 10000,
    requestsPerMinute: 100,
    tokensPerDay: 1000000,
    features: [
      "All pro features",
      "Unlimited access",
      "Admin dashboard",
      "System metrics",
      "Priority support"
    ],
    limitations: []
  }
};

export default function TierLimits({ currentTier, className = "" }: TierLimitsProps) {
  const currentTierData = tierData[currentTier as keyof typeof tierData] || tierData.free;
  
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <div className="text-center mb-6">
        <div className={`w-16 h-16 bg-gradient-to-r ${currentTierData.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
          {currentTierData.icon}
        </div>
        <h3 className="text-2xl font-bold text-gray-900">{currentTierData.name} Plan</h3>
        <p className="text-gray-600 mt-2">Your current subscription tier</p>
      </div>

      {/* Limits Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">{currentTierData.requestsPerDay}</div>
          <div className="text-sm text-blue-800">Requests/Day</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">{currentTierData.requestsPerMinute}</div>
          <div className="text-sm text-green-800">Requests/Minute</div>
        </div>
        <div className="bg-purple-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-purple-600">
            {currentTierData.tokensPerDay >= 1000000 
              ? `${(currentTierData.tokensPerDay / 1000000).toFixed(1)}M`
              : currentTierData.tokensPerDay >= 1000 
                ? `${(currentTierData.tokensPerDay / 1000).toFixed(0)}K`
                : currentTierData.tokensPerDay
            }
          </div>
          <div className="text-sm text-purple-800">Tokens/Day</div>
        </div>
      </div>

      {/* Features */}
      <div className="mb-6">
        <h4 className="text-lg font-semibold text-gray-800 mb-3">Included Features</h4>
        <div className="space-y-2">
          {currentTierData.features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center space-x-2"
            >
              <Check className="h-4 w-4 text-green-500" />
              <span className="text-gray-700">{feature}</span>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Limitations */}
      {currentTierData.limitations.length > 0 && (
        <div className="mb-6">
          <h4 className="text-lg font-semibold text-gray-800 mb-3">Limitations</h4>
          <div className="space-y-2">
            {currentTierData.limitations.map((limitation, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center space-x-2"
              >
                <X className="h-4 w-4 text-red-500" />
                <span className="text-gray-700">{limitation}</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Upgrade CTA for non-admin users */}
      {currentTier !== "admin" && (
        <div className="text-center">
          <button className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all">
            Upgrade Plan
          </button>
        </div>
      )}
    </div>
  );
}
