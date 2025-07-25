import Head from 'next/head'
import Layout from '@/components/Layout'
import { motion } from 'framer-motion'

export default function Vessels() {
  return (
    <Layout>
      <Head>
        <title>Vessel Options - Atlas Fluvial</title>
        <meta name="description" content="Explore vessel options for European waterway travel - charter, purchase, or bring your own boat." />
      </Head>

      <section className="bg-gradient-to-r from-canal to-river text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl font-bold mb-4">Vessel Options</h1>
            <p className="text-xl max-w-3xl">
              Find the perfect vessel for your European waterway adventure.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-white rounded-lg shadow-sm p-8"
            >
              <h2 className="text-2xl font-bold mb-4">Charter a Vessel</h2>
              <p className="text-gray-600 mb-6">
                Perfect for first-time navigators or those seeking a hassle-free experience. Choose from hundreds of 
                well-maintained vessels across Europe.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-ocean mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">No license required options</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-ocean mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Full briefing and support</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-ocean mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Insurance included</span>
                </li>
              </ul>
              <button className="w-full bg-ocean text-white py-2 rounded-lg font-semibold hover:bg-ocean/90">
                View Charter Options
              </button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="bg-white rounded-lg shadow-sm p-8"
            >
              <h2 className="text-2xl font-bold mb-4">Buy a Vessel</h2>
              <p className="text-gray-600 mb-6">
                Make your waterway dreams permanent with vessel ownership. Access our network of trusted brokers 
                and marine surveyors.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-river mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">New and used vessels</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-river mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Purchase guidance</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-river mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Mooring arrangements</span>
                </li>
              </ul>
              <button className="w-full bg-river text-white py-2 rounded-lg font-semibold hover:bg-river/90">
                Browse Vessels for Sale
              </button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="bg-white rounded-lg shadow-sm p-8"
            >
              <h2 className="text-2xl font-bold mb-4">Bring Your Vessel</h2>
              <p className="text-gray-600 mb-6">
                Navigate European waterways with your own vessel. We provide all the information needed for 
                international cruising.
              </p>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-canal mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Transport logistics</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-canal mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Documentation requirements</span>
                </li>
                <li className="flex items-start">
                  <svg className="w-5 h-5 text-canal mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">Technical standards</span>
                </li>
              </ul>
              <button className="w-full bg-canal text-white py-2 rounded-lg font-semibold hover:bg-canal/90">
                Import Guidelines
              </button>
            </motion.div>
          </div>

          <div className="bg-gray-50 rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-center">Vessel Requirements by Country</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">License Required</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Max Length</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Equipment</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">France</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">ICC or equivalent</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">15m without</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Standard EU</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Netherlands</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Vaarbewijs</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">15m</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Enhanced safety</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Germany</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Sportbootführerschein</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">20m</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Standard EU</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}