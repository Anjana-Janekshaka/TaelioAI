"use client";

import { motion } from "framer-motion";
import { BarChart3, TrendingUp, DollarSign, Clock, Zap, AlertCircle } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { apiService } from "@/lib/api";

interface UserUsage {
  user_id: string;
  email: string;
  role: string;
  period_days: number;
  total_requests: number;
  total_tokens_in: number;
  total_tokens_out: number;
  total_cost: number;
  feature_breakdown: Record<string, any>;
}

interface UserProfile {
  user_id: string;
  email: string;
  role: string;
  tier: string;
}

interface TierInfo {
  user_id: string;
  email: string;
  tier: string;
  role: string;
  limits: Record<string, any>;
  current_usage: Record<string, any>;
  remaining: Record<string, any>;
}

interface UserMetricsDropdownProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function UserMetricsDropdown({ isOpen, onClose }: UserMetricsDropdownProps) {
  const [usage, setUsage] = useState<UserUsage | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [tierInfo, setTierInfo] = useState<TierInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      fetchUserMetrics();
    }
  }, [isOpen]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  const fetchUserMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const [usageData, profileData, tierInfoData] = await Promise.all([
        apiService.getUserUsage(30),
        apiService.getUserProfile(),
        apiService.getUserTierInfo()
      ]);
      setUsage(usageData);
      setProfile(profileData);
      setTierInfo(tierInfoData);
    } catch (err) {
      console.error('Failed to fetch user metrics:', err);
      setError('Failed to load metrics');
    } finally {
      setLoading(false);
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  const formatCurrency = (amount: number) => {
    return `$${amount.toFixed(4)}`;
  };

  if (!isOpen) return null;

  return (
    <motion.div
      ref={dropdownRef}
      initial={{ opacity: 0, y: -10, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -10, scale: 0.95 }}
      transition={{ duration: 0.2 }}
      className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-200 py-4 z-50"
    >
      {/* Header */}
      <div className="px-4 pb-3 border-b border-gray-100">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-blue-100 rounded-lg">
            <BarChart3 className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">Usage Metrics</h3>
            <p className="text-sm text-gray-500">Last 30 days</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="px-4 py-3">
        {loading ? (
          <div className="space-y-3">
            <div className="animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="animate-pulse">
                <div className="h-8 bg-gray-200 rounded mb-1"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
              <div className="animate-pulse">
                <div className="h-8 bg-gray-200 rounded mb-1"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
            </div>
          </div>
        ) : error ? (
          <div className="text-center py-4">
            <AlertCircle className="h-8 w-8 text-red-500 mx-auto mb-2" />
            <p className="text-red-600 text-sm">{error}</p>
            <button 
              onClick={fetchUserMetrics}
              className="mt-2 px-3 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
            >
              Retry
            </button>
          </div>
        ) : usage ? (
          <div className="space-y-4">
            {/* Key Metrics */}
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-blue-50 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-1">
                  <TrendingUp className="h-4 w-4 text-blue-600" />
                  <span className="text-xs font-medium text-blue-800">Requests</span>
                </div>
                <div className="text-lg font-bold text-blue-900">
                  {formatNumber(usage.total_requests)}
                </div>
              </div>
              
              <div className="bg-green-50 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-1">
                  <DollarSign className="h-4 w-4 text-green-600" />
                  <span className="text-xs font-medium text-green-800">Cost</span>
                </div>
                <div className="text-lg font-bold text-green-900">
                  {formatCurrency(usage.total_cost)}
                </div>
              </div>
            </div>

            {/* Token Usage */}
            <div className="bg-gray-50 rounded-lg p-3">
              <div className="flex items-center space-x-2 mb-2">
                <Zap className="h-4 w-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-800">Token Usage</span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <span className="text-gray-600">Input:</span>
                  <span className="font-semibold ml-1">{formatNumber(usage.total_tokens_in)}</span>
                </div>
                <div>
                  <span className="text-gray-600">Output:</span>
                  <span className="font-semibold ml-1">{formatNumber(usage.total_tokens_out)}</span>
                </div>
              </div>
            </div>

            {/* Tier Information */}
            {tierInfo && (
              <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <Zap className="h-4 w-4 text-blue-600" />
                  <span className="text-sm font-medium text-blue-800">Current Plan</span>
                </div>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Tier:</span>
                    <span className="font-semibold text-blue-900 capitalize">{tierInfo.tier}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Role:</span>
                    <span className="font-semibold text-blue-900 capitalize">{tierInfo.role}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Remaining Limits */}
            {tierInfo && tierInfo.remaining && (
              <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <Clock className="h-4 w-4 text-green-600" />
                  <span className="text-sm font-medium text-green-800">Remaining Today</span>
                </div>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Requests:</span>
                    <span className="font-semibold text-green-900">
                      {tierInfo.remaining.requests_today || 0} / {tierInfo.limits?.requests_per_day || 50}
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Tokens:</span>
                    <span className="font-semibold text-green-900">
                      {tierInfo.remaining.tokens_today || 0} / {tierInfo.limits?.tokens_per_day || 10000}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {/* Feature Breakdown */}
            {usage.feature_breakdown && Object.keys(usage.feature_breakdown).length > 0 && (
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <BarChart3 className="h-4 w-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-800">Features Used</span>
                </div>
                <div className="space-y-1">
                  {Object.entries(usage.feature_breakdown).map(([feature, data]: [string, any]) => (
                    <div key={feature} className="flex justify-between items-center text-xs">
                      <span className="text-gray-600 capitalize">
                        {feature.replace('_', ' ')}
                      </span>
                      <span className="font-semibold text-gray-800">
                        {data.requests || 0}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* View Full Metrics Link */}
            <div className="pt-2 border-t border-gray-100">
              <a 
                href="/metrics"
                className="flex items-center justify-center space-x-2 text-blue-600 hover:text-blue-700 text-sm font-medium"
              >
                <BarChart3 className="h-4 w-4" />
                <span>View Full Metrics</span>
              </a>
            </div>
          </div>
        ) : (
          <div className="text-center py-4">
            <BarChart3 className="h-8 w-8 text-gray-400 mx-auto mb-2" />
            <p className="text-gray-500 text-sm">No usage data available</p>
          </div>
        )}
      </div>
    </motion.div>
  );
}
