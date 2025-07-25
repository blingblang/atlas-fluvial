import Head from 'next/head'
import Layout from '@/components/Layout'
import { motion } from 'framer-motion'

export default function Resources() {
  return (
    <Layout>
      <Head>
        <title>Resources - Atlas Fluvial</title>
        <meta name="description" content="Essential resources for European waterway navigation - weather, regulations, emergency contacts, and more." />
      </Head>

      <section className="bg-gradient-to-r from-atlas-dark to-canal text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl font-bold mb-4">Navigation Resources</h1>
            <p className="text-xl max-w-3xl">
              Essential tools and information for safe and successful waterway navigation.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold mb-4">Weather & Water Levels</h2>
              <p className="text-gray-600 mb-4">
                Stay informed with real-time weather conditions and water level monitoring across European waterways.
              </p>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-ocean hover:text-river font-medium">European Weather Service →</a>
                  <p className="text-sm text-gray-500">Multi-day forecasts for all regions</p>
                </li>
                <li>
                  <a href="#" className="text-ocean hover:text-river font-medium">Water Level Monitoring →</a>
                  <p className="text-sm text-gray-500">Real-time gauge readings</p>
                </li>
                <li>
                  <a href="#" className="text-ocean hover:text-river font-medium">Navigation Warnings →</a>
                  <p className="text-sm text-gray-500">Current restrictions and closures</p>
                </li>
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-2xl font-bold mb-4">Regulations & Documentation</h2>
              <p className="text-gray-600 mb-4">
                Comprehensive guides to international waterway regulations and required documentation.
              </p>
              <ul className="space-y-3">
                <li>
                  <a href="#" className="text-ocean hover:text-river font-medium">License Requirements →</a>
                  <p className="text-sm text-gray-500">Country-specific boating licenses</p>
                </li>
                <li>
                  <a href="#" className="text-ocean hover:text-river font-medium">Customs & Immigration →</a>
                  <p className="text-sm text-gray-500">Border crossing procedures</p>
                </li>
                <li>
                  <a href="#" className="text-ocean hover:text-river font-medium">Insurance Guidelines →</a>
                  <p className="text-sm text-gray-500">Coverage requirements by country</p>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-8 mb-12">
            <h2 className="text-2xl font-bold mb-6">Emergency Contacts</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h3 className="font-semibold mb-3">General Emergency</h3>
                <p className="text-2xl font-bold text-red-600 mb-2">112</p>
                <p className="text-sm text-gray-600">Valid in all EU countries</p>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Water Police</h3>
                <p className="text-lg font-medium mb-2">Country-specific</p>
                <a href="#" className="text-ocean text-sm hover:text-river">View directory →</a>
              </div>
              <div>
                <h3 className="font-semibold mb-3">Canal Authorities</h3>
                <p className="text-lg font-medium mb-2">VHF Channel 10</p>
                <p className="text-sm text-gray-600">Standard in most regions</p>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="w-12 h-12 bg-ocean/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-ocean" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Language Guide</h3>
              <p className="text-gray-600 text-sm mb-4">Essential nautical terms in 6 languages</p>
              <a href="#" className="text-ocean hover:text-river font-medium text-sm">Download PDF →</a>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="w-12 h-12 bg-river/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-river" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Marina Directory</h3>
              <p className="text-gray-600 text-sm mb-4">2,000+ marinas with facilities info</p>
              <a href="#" className="text-river hover:text-ocean font-medium text-sm">Search Marinas →</a>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="w-12 h-12 bg-canal/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-canal" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Lock Operations</h3>
              <p className="text-gray-600 text-sm mb-4">Operating times and contact info</p>
              <a href="#" className="text-canal hover:text-river font-medium text-sm">View Schedule →</a>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}