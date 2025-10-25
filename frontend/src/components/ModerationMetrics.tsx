'use client';

import React, { useState, useEffect } from 'react';
import { apiService, ModerationMetrics, ModerationStats } from '@/lib/api';

interface ModerationMetricsProps {
  className?: string;
}

const ModerationMetrics: React.FC<ModerationMetricsProps> = ({ className = '' }) => {
  const [metrics, setMetrics] = useState<ModerationMetrics | null>(null);
  const [stats, setStats] = useState<ModerationStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState(30);

  useEffect(() => {
    fetchModerationData();
  }, [selectedPeriod]);

  const fetchModerationData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [metricsData, statsData] = await Promise.all([
        apiService.getModerationMetrics(selectedPeriod),
        apiService.getModerationStats(selectedPeriod)
      ]);
      
      setMetrics(metricsData);
      setStats(statsData);
    } catch (err) {
      console.error('Failed to fetch moderation data:', err);
      setError('Failed to load moderation metrics');
    } finally {
      setLoading(false);
    }
  };

  const getSafetyScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    if (score >= 50) return 'text-orange-600';
    return 'text-red-600';
  };

  const getSafetyScoreLabel = (score: number) => {
    if (score >= 90) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 50) return 'Fair';
    return 'Poor';
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded w-5/6"></div>
            <div className="h-4 bg-gray-200 rounded w-4/6"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="text-center">
          <div className="text-red-600 mb-2">⚠️</div>
          <p className="text-red-600">{error}</p>
          <button 
            onClick={fetchModerationData}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!metrics || !stats) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <p className="text-gray-500">No moderation data available</p>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Content Moderation Metrics</h2>
        <div className="flex items-center space-x-2">
          <label htmlFor="period" className="text-sm font-medium text-gray-700">
            Period:
          </label>
          <select
            id="period"
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(Number(e.target.value))}
            className="border border-gray-300 rounded px-3 py-1 text-sm"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-blue-600">{metrics.total_content_moderated}</div>
          <div className="text-sm text-blue-800">Content Moderated</div>
        </div>
        
        <div className="bg-red-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-red-600">{metrics.total_violations_found}</div>
          <div className="text-sm text-red-800">Violations Found</div>
        </div>
        
        <div className="bg-orange-50 rounded-lg p-4">
          <div className="text-2xl font-bold text-orange-600">{metrics.total_unsafe_content}</div>
          <div className="text-sm text-orange-800">Unsafe Content</div>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4">
          <div className={`text-2xl font-bold ${getSafetyScoreColor(metrics.average_safety_score)}`}>
            {metrics.average_safety_score.toFixed(1)}
          </div>
          <div className="text-sm text-green-800">Avg Safety Score</div>
        </div>
      </div>

      {/* Detailed Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Violations by Type */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Violations by Type</h3>
          <div className="space-y-3">
            {Object.entries(metrics.violations_by_type).map(([type, count]) => (
              <div key={type} className="flex justify-between items-center">
                <span className="text-sm text-gray-600 capitalize">
                  {type.replace('_', ' ')}
                </span>
                <span className="font-semibold text-gray-800">{count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Content by Type */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Content by Type</h3>
          <div className="space-y-3">
            {Object.entries(metrics.content_by_type).map(([type, count]) => (
              <div key={type} className="flex justify-between items-center">
                <span className="text-sm text-gray-600 capitalize">{type}</span>
                <span className="font-semibold text-gray-800">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Safety Score Distribution */}
      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Safety Score Distribution</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(metrics.safety_score_distribution).map(([range, count]) => (
            <div key={range} className="bg-gray-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-gray-800">{count}</div>
              <div className="text-sm text-gray-600">{range}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Violation Breakdown */}
      {stats.violation_breakdown.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Violation Breakdown</h3>
          <div className="space-y-3">
            {stats.violation_breakdown.map((violation, index) => (
              <div key={index} className="bg-gray-50 rounded-lg p-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium text-gray-800 capitalize">
                    {violation.violation_type.replace('_', ' ')}
                  </span>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    violation.severity === 'high' ? 'bg-red-100 text-red-800' :
                    violation.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {violation.severity}
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm text-gray-600">
                  <span>{violation.count} violations</span>
                  <span>{violation.percentage}% of content</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="mt-6 bg-blue-50 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Summary</h3>
        <p className="text-gray-600">
          Over the last {selectedPeriod} days, {metrics.total_content_moderated} pieces of content 
          were moderated with an average safety score of {metrics.average_safety_score.toFixed(1)} 
          ({getSafetyScoreLabel(metrics.average_safety_score)}). 
          {metrics.total_violations_found > 0 && (
            <> {metrics.total_violations_found} violations were found and {metrics.total_unsafe_content} 
            pieces of content were flagged as unsafe.</>
          )}
        </p>
      </div>
    </div>
  );
};

export default ModerationMetrics;
