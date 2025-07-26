import React from 'react';
import Layout from '../../components/Layout';
import WaterwaysAssistant from '../../components/WaterwaysAssistant';

const WaterwaysAssistantPage: React.FC = () => {
  return (
    <Layout>
      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
        {/* Hero Section */}
        <section className="py-12 px-4">
          <div className="max-w-7xl mx-auto text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI Waterways Assistant
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Get instant, accurate information about French waterways using our RAG-enhanced AI assistant.
              Ask about navigation, locks, elevations, routes, and more.
            </p>
          </div>
        </section>

        {/* Assistant Widget */}
        <section className="py-8 px-4">
          <WaterwaysAssistant />
        </section>

        {/* Features Section */}
        <section className="py-12 px-4">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-2xl font-bold text-center mb-8">Intelligent Waterways Information</h2>
            
            <div className="grid md:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-blue-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5s3.332.477 4.5 1.253v13c-1.168-.776-2.754-1.253-4.5-1.253s-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="font-semibold mb-2">Comprehensive Database</h3>
                <p className="text-sm text-gray-600">
                  Access detailed information about all major French waterways, including rivers, canals, and lakes.
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-blue-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h3 className="font-semibold mb-2">RAG Technology</h3>
                <p className="text-sm text-gray-600">
                  Combines AI with real data retrieval for accurate, up-to-date waterway information.
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-blue-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                </div>
                <h3 className="font-semibold mb-2">Natural Language</h3>
                <p className="text-sm text-gray-600">
                  Ask questions in plain English and get clear, detailed answers about navigation and waterways.
                </p>
              </div>

              <div className="bg-white p-6 rounded-lg shadow-md">
                <div className="text-blue-600 mb-3">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 className="font-semibold mb-2">Verified Sources</h3>
                <p className="text-sm text-gray-600">
                  Information is sourced from official navigation guides and verified databases.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Query Categories */}
        <section className="py-12 px-4 bg-gray-50">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-2xl font-bold text-center mb-8">What You Can Ask</h2>
            
            <div className="grid md:grid-cols-3 gap-8">
              <div>
                <h3 className="font-semibold text-lg mb-3 text-blue-600">Navigation & Routes</h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    Which waterways connect Paris to the Mediterranean?
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    What's the best route from Lyon to Marseille by boat?
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    Can I navigate from the Atlantic to the Mediterranean?
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-blue-600">Technical Information</h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    What's the maximum draft allowed on the Seine?
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    How many locks are on the Canal du Midi?
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    What's the air draft clearance under bridges?
                  </li>
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-lg mb-3 text-blue-600">Location & Elevation</h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    What's the elevation of the canal near Toulouse?
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    Find waterways near Carcassonne
                  </li>
                  <li className="flex items-start">
                    <span className="text-blue-500 mr-2">•</span>
                    Which rivers flow through Avignon?
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-12 px-4 bg-blue-600 text-white">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4">Start Planning Your Journey</h2>
            <p className="text-xl mb-8 opacity-90">
              Our AI assistant is ready to help you navigate French waterways with confidence.
              Ask any question about routes, locks, elevations, or navigation requirements.
            </p>
            <div className="flex justify-center space-x-4">
              <a
                href="#top"
                className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                Ask a Question
              </a>
              <a
                href="/waterways"
                className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                Explore Waterways
              </a>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default WaterwaysAssistantPage;