import Head from 'next/head'
import Image from 'next/image'
import Link from 'next/link'
import Layout from '@/components/Layout'
import { motion } from 'framer-motion'

export default function Home() {
  return (
    <Layout>
      <Head>
        <title>Atlas Fluvial - Navigate European Waterways</title>
        <meta name="description" content="Your comprehensive guide to exploring Europe's canals, rivers, and waterways. Plan your journey with confidence using our detailed navigation guides and resources." />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-ocean/90 to-river/90 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Navigate Europe's Waterways
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
              Discover the freedom of exploring Europe's intricate network of canals and rivers at your own pace.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/waterways" className="bg-white text-ocean px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                Explore Waterways
              </Link>
              <Link href="/planning" className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-ocean transition-colors">
                Plan Your Journey
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Your Complete Navigation Resource
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Whether you're planning your first canal journey or you're an experienced navigator, Atlas Fluvial provides everything you need.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-gray-50 rounded-lg p-6"
            >
              <div className="w-12 h-12 bg-ocean/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-ocean" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Detailed Waterway Maps</h3>
              <p className="text-gray-600">
                Interactive maps covering over 40,000 kilometers of navigable waterways across 19 European countries.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="bg-gray-50 rounded-lg p-6"
            >
              <div className="w-12 h-12 bg-river/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-river" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Navigation Guides</h3>
              <p className="text-gray-600">
                Comprehensive guides with lock information, mooring locations, and essential navigation details for safe passage.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="bg-gray-50 rounded-lg p-6"
            >
              <div className="w-12 h-12 bg-canal/10 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-canal" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Vessel Information</h3>
              <p className="text-gray-600">
                Everything you need to know about chartering, purchasing, or bringing your own vessel to European waterways.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Journey Types Section */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Choose Your Adventure
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              From peaceful canal cruising to navigating major rivers, find the perfect waterway journey for your experience level and interests.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="p-8">
                <h3 className="text-2xl font-semibold mb-4">Canal Cruising</h3>
                <p className="text-gray-600 mb-6">
                  Experience the tranquility of historic canals, navigate through charming locks, and discover hidden villages accessible only by water. Perfect for beginners and those seeking a relaxed pace.
                </p>
                <ul className="space-y-2 mb-6">
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-ocean mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Calm waters ideal for beginners</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-ocean mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Historic locks and aqueducts</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-ocean mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Scenic countryside routes</span>
                  </li>
                </ul>
                <Link href="/waterways?type=canal" className="text-ocean font-semibold hover:text-river">
                  Explore Canal Routes →
                </Link>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="p-8">
                <h3 className="text-2xl font-semibold mb-4">River Navigation</h3>
                <p className="text-gray-600 mb-6">
                  Navigate Europe's major rivers, from the romantic Rhine to the majestic Danube. Experience dynamic waterways with stronger currents and spectacular scenery.
                </p>
                <ul className="space-y-2 mb-6">
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-river mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Major European cities accessible</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-river mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Dramatic landscapes and castles</span>
                  </li>
                  <li className="flex items-start">
                    <svg className="w-5 h-5 text-river mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-700">Professional navigation skills required</span>
                  </li>
                </ul>
                <Link href="/waterways?type=river" className="text-river font-semibold hover:text-ocean">
                  Explore River Routes →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-ocean text-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to Start Your Journey?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Access comprehensive guides, detailed maps, and expert advice to navigate European waterways with confidence.
          </p>
          <Link href="/guides" className="bg-white text-ocean px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-block">
            View Navigation Guides
          </Link>
        </div>
      </section>
    </Layout>
  )
}