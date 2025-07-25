import Head from 'next/head'
import Layout from '@/components/Layout'
import { motion } from 'framer-motion'

export default function Planning() {
  return (
    <Layout>
      <Head>
        <title>Journey Planning - Atlas Fluvial</title>
        <meta name="description" content="Plan your perfect waterway journey with our comprehensive planning tools and expert advice." />
      </Head>

      <section className="bg-gradient-to-r from-river to-canal text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl font-bold mb-4">Journey Planning</h1>
            <p className="text-xl max-w-3xl">
              Transform your waterway dreams into reality with our comprehensive planning resources.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-semibold mb-4">Route Planning</h3>
              <p className="text-gray-600 mb-4">
                Design your perfect itinerary with our route planning tools. Calculate distances, lock counts, and estimated journey times.
              </p>
              <ul className="space-y-2 text-gray-700">
                <li>• Interactive route builder</li>
                <li>• Distance calculations</li>
                <li>• Lock and bridge information</li>
                <li>• Fuel stop locations</li>
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-semibold mb-4">Seasonal Considerations</h3>
              <p className="text-gray-600 mb-4">
                Navigate year-round with confidence. Understanding seasonal variations in water levels, weather, and operating hours.
              </p>
              <ul className="space-y-2 text-gray-700">
                <li>• Best travel seasons by region</li>
                <li>• Water level monitoring</li>
                <li>• Winter closures</li>
                <li>• Festival calendars</li>
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-xl font-semibold mb-4">Essential Preparation</h3>
              <p className="text-gray-600 mb-4">
                Ensure smooth sailing with our comprehensive preparation checklists and requirement guides.
              </p>
              <ul className="space-y-2 text-gray-700">
                <li>• License requirements</li>
                <li>• Equipment checklists</li>
                <li>• Documentation needs</li>
                <li>• Safety protocols</li>
              </ul>
            </div>
          </div>

          <div className="mt-16 bg-gray-50 rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-6 text-center">Journey Duration Calculator</h2>
            <div className="max-w-2xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Starting Point</label>
                  <input type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" placeholder="e.g., Amsterdam" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Destination</label>
                  <input type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" placeholder="e.g., Paris" />
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Average Speed (km/h)</label>
                  <input type="number" className="w-full px-4 py-2 border border-gray-300 rounded-lg" placeholder="8" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Hours per Day</label>
                  <input type="number" className="w-full px-4 py-2 border border-gray-300 rounded-lg" placeholder="6" />
                </div>
              </div>
              <button className="w-full bg-ocean text-white py-3 rounded-lg font-semibold hover:bg-ocean/90">
                Calculate Journey Time
              </button>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  )
}