import React from 'react';
import Layout from '../../components/Layout';
import Link from 'next/link';

const ToolsPage: React.FC = () => {
  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
        {/* Hero Section */}
        <section className="py-12 px-4">
          <div className="max-w-7xl mx-auto text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Navigation Tools
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Advanced digital tools to enhance your waterway navigation experience.
            </p>
          </div>
        </section>

        {/* Tools Grid */}
        <section className="py-8 px-4">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-2xl font-bold text-center mb-8">Available Tools</h2>
            
            <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
              <Link href="/tools/waterways-assistant" className="block">
                <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer h-full">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-2xl">🤖</span>
                    </div>
                    <h3 className="text-xl font-semibold">AI Waterways Assistant</h3>
                  </div>
                  <p className="text-gray-600 mb-4">
                    Get instant answers about French waterways using our RAG-enhanced AI. Ask about navigation, locks, elevations, routes, and more.
                  </p>
                  <div className="text-blue-600 font-semibold flex items-center">
                    Try the Assistant
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>

              <Link href="/tools/elevation" className="block">
                <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer h-full">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                      <span className="text-2xl">📏</span>
                    </div>
                    <h3 className="text-xl font-semibold">Elevation Finder</h3>
                  </div>
                  <p className="text-gray-600 mb-4">
                    Find precise elevation data for any French river segment. Search by river name or coordinates using RiverATLAS data.
                  </p>
                  <div className="text-blue-600 font-semibold flex items-center">
                    Check Elevations
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            </div>

            {/* Coming Soon Section */}
            <div className="mt-12 bg-blue-50 rounded-lg p-8">
              <h3 className="text-xl font-semibold mb-6 text-center">Coming Soon</h3>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="bg-white p-4 rounded">
                  <h4 className="font-semibold mb-2">Route Calculator</h4>
                  <p className="text-sm text-gray-600">
                    Calculate optimal routes between any two points on the waterway network.
                  </p>
                </div>
                <div className="bg-white p-4 rounded">
                  <h4 className="font-semibold mb-2">Lock Timer</h4>
                  <p className="text-sm text-gray-600">
                    Estimate journey times including lock passages and waiting times.
                  </p>
                </div>
                <div className="bg-white p-4 rounded">
                  <h4 className="font-semibold mb-2">Mooring Finder</h4>
                  <p className="text-sm text-gray-600">
                    Locate available moorings with real-time availability updates.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default ToolsPage;