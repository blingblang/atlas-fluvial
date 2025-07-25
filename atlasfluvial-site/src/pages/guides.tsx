import Head from 'next/head'
import Layout from '@/components/Layout'
import Link from 'next/link'
import { motion } from 'framer-motion'

const guides = [
  {
    title: 'French Waterways Navigator',
    edition: '2025 Edition',
    coverage: 'Complete coverage of 8,500km of French canals and rivers',
    features: ['480 pages', 'Full-color maps', 'Lock details', 'Mooring guides'],
    price: '€89',
  },
  {
    title: 'Rhine & Moselle Guide',
    edition: '2025 Edition',
    coverage: 'Comprehensive guide from Basel to Rotterdam',
    features: ['320 pages', 'Navigation charts', 'Port information', 'Cultural insights'],
    price: '€79',
  },
  {
    title: 'Danube Complete',
    edition: '2025 Edition',
    coverage: 'From Black Forest to Black Sea - 10 countries covered',
    features: ['520 pages', 'Multi-language support', 'Border crossings', 'Marina directory'],
    price: '€95',
  },
  {
    title: 'Dutch Waterways Handbook',
    edition: '2025 Edition',
    coverage: 'Netherlands complete with Amsterdam detail maps',
    features: ['280 pages', 'Bridge clearances', 'Cycling routes', 'City guides'],
    price: '€69',
  },
]

export default function Guides() {
  return (
    <Layout>
      <Head>
        <title>Navigation Guides - Atlas Fluvial</title>
        <meta name="description" content="Professional navigation guides for European waterways. Detailed charts, lock information, and essential cruising data." />
      </Head>

      <section className="bg-gradient-to-r from-ocean to-atlas-dark text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl font-bold mb-4">Navigation Guides</h1>
            <p className="text-xl max-w-3xl">
              Professional-grade navigation resources trusted by thousands of waterway travelers across Europe.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">2025 Edition Guides</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Updated annually with the latest navigation information, infrastructure changes, and regulatory updates.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {guides.map((guide, index) => (
              <motion.div
                key={guide.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white rounded-lg shadow-sm overflow-hidden"
              >
                <div className="p-8">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-2xl font-semibold">{guide.title}</h3>
                      <p className="text-ocean font-medium">{guide.edition}</p>
                    </div>
                    <span className="text-2xl font-bold text-gray-900">{guide.price}</span>
                  </div>
                  <p className="text-gray-600 mb-6">{guide.coverage}</p>
                  <ul className="space-y-2 mb-6">
                    {guide.features.map((feature) => (
                      <li key={feature} className="flex items-center text-gray-700">
                        <svg className="w-5 h-5 text-ocean mr-2" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <button className="w-full bg-ocean text-white py-3 rounded-lg font-semibold hover:bg-ocean/90 transition-colors">
                    View Details
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          <div className="mt-16 bg-gray-50 rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-center">Digital Navigation Suite</h2>
            <div className="max-w-3xl mx-auto">
              <p className="text-gray-600 mb-8 text-center">
                Access all our guides digitally with real-time updates, offline downloads, and interactive features.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-ocean/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-ocean" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Mobile Access</h3>
                  <p className="text-gray-600 text-sm">Navigate on any device with our responsive app</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-river/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-river" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Offline Maps</h3>
                  <p className="text-gray-600 text-sm">Download regions for offline navigation</p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-canal/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-canal" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
                    </svg>
                  </div>
                  <h3 className="font-semibold mb-2">Live Updates</h3>
                  <p className="text-gray-600 text-sm">Real-time navigation notices and changes</p>
                </div>
              </div>
              <div className="text-center">
                <button className="bg-atlas-dark text-white px-8 py-3 rounded-lg font-semibold hover:bg-gray-800 transition-colors">
                  Start Free Trial
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}