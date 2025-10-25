"use client";

import { motion } from "framer-motion";
import { Sparkles, Menu, X, User, LogOut, Crown, Zap, BarChart3 } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { user, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const userMenuRef = useRef<HTMLDivElement>(null);

  // Close user menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
    };

    if (showUserMenu) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [showUserMenu]);

  const handleLogout = () => {
    logout();
    router.push('/');
    setShowUserMenu(false);
  };

  const getTierIcon = (role: string) => {
    switch (role) {
      case 'pro':
        return <Crown className="h-4 w-4 text-yellow-500" />;
      case 'admin':
        return <Zap className="h-4 w-4 text-purple-500" />;
      default:
        return <User className="h-4 w-4 text-gray-500" />;
    }
  };

  const getTierName = (role: string) => {
    switch (role) {
      case 'pro':
        return 'Pro';
      case 'admin':
        return 'Admin';
      default:
        return 'Free';
    }
  };

  const getTierColor = (role: string) => {
    switch (role) {
      case 'pro':
        return 'from-yellow-500 to-orange-500';
      case 'admin':
        return 'from-purple-500 to-pink-500';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <motion.header
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200"
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-2"
          >
            <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <span className="text-2xl font-bold gradient-text">
              TaelioAI
            </span>
          </motion.div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-gray-600 hover:text-blue-600 transition-colors">
              Features
            </a>
            <a href="#workflow" className="text-gray-600 hover:text-blue-600 transition-colors">
              Workflow
            </a>
            {isAuthenticated && (
              <a href="/metrics" className="text-gray-600 hover:text-blue-600 transition-colors flex items-center space-x-1">
                <BarChart3 className="h-4 w-4" />
                <span>Metrics</span>
              </a>
            )}
            <a href="#about" className="text-gray-600 hover:text-blue-600 transition-colors">
              About
            </a>
            
            {isAuthenticated ? (
              /* User Menu */
              <div className="relative" ref={userMenuRef}>
                <motion.button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="flex items-center space-x-3 px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-gray-200 hover:border-gray-300 transition-all"
                >
                  <div className="flex items-center space-x-2">
                    <div className={`w-8 h-8 bg-gradient-to-r ${getTierColor(user?.role || 'free')} rounded-full flex items-center justify-center`}>
                      {getTierIcon(user?.role || 'free')}
                    </div>
                    <div className="text-left">
                      <div className="text-sm font-medium text-gray-900">
                        {user?.email?.split('@')[0] || 'User'}
                      </div>
                      <div className="text-xs text-gray-500 flex items-center space-x-1">
                        {getTierIcon(user?.role || 'free')}
                        <span>{getTierName(user?.role || 'free')}</span>
                      </div>
                    </div>
                  </div>
                </motion.button>

                {/* User Dropdown Menu */}
                {showUserMenu && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                  >
                    <div className="px-4 py-3 border-b border-gray-100">
                      <div className="flex items-center space-x-3">
                        <div className={`w-10 h-10 bg-gradient-to-r ${getTierColor(user?.role || 'free')} rounded-full flex items-center justify-center`}>
                          {getTierIcon(user?.role || 'free')}
                        </div>
                        <div>
                          <div className="font-medium text-gray-900">{user?.email}</div>
                          <div className="text-sm text-gray-500 flex items-center space-x-1">
                            {getTierIcon(user?.role || 'free')}
                            <span>{getTierName(user?.role || 'free')} Plan</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <div className="py-2">
                      <a href="/metrics" className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center space-x-2">
                        <BarChart3 className="h-4 w-4" />
                        <span>Metrics</span>
                      </a>
                      <button className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center space-x-2">
                        <User className="h-4 w-4" />
                        <span>Profile</span>
                      </button>
                      <button className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 flex items-center space-x-2">
                        <Crown className="h-4 w-4" />
                        <span>Upgrade Plan</span>
                      </button>
                      <button 
                        onClick={handleLogout}
                        className="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 flex items-center space-x-2"
                      >
                        <LogOut className="h-4 w-4" />
                        <span>Sign Out</span>
                      </button>
                    </div>
                  </motion.div>
                )}
              </div>
            ) : (
              /* Guest Navigation */
              <div className="flex items-center space-x-4">
                <a
                  href="/login"
                  className="text-gray-600 hover:text-blue-600 transition-colors"
                >
                  Sign In
                </a>
                <motion.a
                  href="/register"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all"
                >
                  Get Started
                </motion.a>
              </div>
            )}
          </nav>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden p-2"
          >
            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <motion.nav
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden mt-4 pb-4 border-t border-gray-200"
          >
            <div className="flex flex-col space-y-4 pt-4">
              <a href="#features" className="text-gray-600 hover:text-blue-600 transition-colors">
                Features
              </a>
              <a href="#workflow" className="text-gray-600 hover:text-blue-600 transition-colors">
                Workflow
              </a>
              {isAuthenticated && (
                <a href="/metrics" className="text-gray-600 hover:text-blue-600 transition-colors flex items-center space-x-2">
                  <BarChart3 className="h-4 w-4" />
                  <span>Metrics</span>
                </a>
              )}
              <a href="#about" className="text-gray-600 hover:text-blue-600 transition-colors">
                About
              </a>
              
              {isAuthenticated ? (
                /* Mobile User Menu */
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-gray-200">
                    <div className={`w-10 h-10 bg-gradient-to-r ${getTierColor(user?.role || 'free')} rounded-full flex items-center justify-center`}>
                      {getTierIcon(user?.role || 'free')}
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">{user?.email}</div>
                      <div className="text-sm text-gray-500 flex items-center space-x-1">
                        {getTierIcon(user?.role || 'free')}
                        <span>{getTierName(user?.role || 'free')} Plan</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <a href="/metrics" className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2">
                      <BarChart3 className="h-4 w-4" />
                      <span>Metrics</span>
                    </a>
                    <button className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2">
                      <User className="h-4 w-4" />
                      <span>Profile</span>
                    </button>
                    <button className="w-full px-4 py-2 text-left text-gray-700 hover:bg-gray-50 rounded-lg flex items-center space-x-2">
                      <Crown className="h-4 w-4" />
                      <span>Upgrade Plan</span>
                    </button>
                    <button 
                      onClick={handleLogout}
                      className="w-full px-4 py-2 text-left text-red-600 hover:bg-red-50 rounded-lg flex items-center space-x-2"
                    >
                      <LogOut className="h-4 w-4" />
                      <span>Sign Out</span>
                    </button>
                  </div>
                </div>
              ) : (
                /* Mobile Guest Navigation */
                <div className="space-y-4">
                  <a href="/login" className="text-gray-600 hover:text-blue-600 transition-colors">
                    Sign In
                  </a>
                  <a href="/register" className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transition-all text-center">
                    Get Started
                  </a>
                </div>
              )}
            </div>
          </motion.nav>
        )}
      </div>
    </motion.header>
  );
}
