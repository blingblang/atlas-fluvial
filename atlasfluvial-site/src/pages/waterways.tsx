import Head from 'next/head'
import Link from 'next/link'
import Layout from '@/components/Layout'
import { motion } from 'framer-motion'

const countries = [
  { name: 'France', waterways: '8,500 km', highlight: 'Canal du Midi, Seine, Rhône' },
  { name: 'Netherlands', waterways: '6,200 km', highlight: 'Amsterdam Canals, IJsselmeer' },
  { name: 'Germany', waterways: '7,300 km', highlight: 'Rhine, Main-Danube Canal' },
  { name: 'Belgium', waterways: '2,000 km', highlight: 'Albert Canal, Meuse' },
  { name: 'United Kingdom', waterways: '3,200 km', highlight: 'Thames, Grand Union Canal' },
  { name: 'Italy', waterways: '2,400 km', highlight: 'Po River, Venetian Lagoon' },
  { name: 'Poland', waterways: '3,600 km', highlight: 'Vistula, Oder' },
  { name: 'Austria', waterways: '358 km', highlight: 'Danube' },
  { name: 'Czech Republic', waterways: '664 km', highlight: 'Elbe, Vltava' },
  { name: 'Hungary', waterways: '1,622 km', highlight: 'Danube, Tisza' },
  { name: 'Romania', waterways: '1,779 km', highlight: 'Danube, Danube-Black Sea Canal' },
  { name: 'Croatia', waterways: '785 km', highlight: 'Sava, Drava' },
]

export default function Waterways() {
  return (
    <Layout>
      <Head>
        <title>European Waterways - Atlas Fluvial</title>
        <meta name="description" content="Explore navigable waterways across 19 European countries. Detailed maps and information for canals, rivers, and lakes." />
      </Head>

      {/* Header */}
      <section className="bg-gradient-to-r from-ocean to-river text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl font-bold mb-4">European Waterways</h1>
            <p className="text-xl max-w-3xl">
              Over 40,000 kilometers of navigable waterways connecting cities, towns, and countryside across Europe.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Interactive Map Placeholder */}
      <section className="py-12 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <h2 className="text-2xl font-bold mb-4">Interactive Waterway Map</h2>
            <div className="bg-gray-100 rounded-lg h-96 flex items-center justify-center">
              <p className="text-gray-500">Interactive map coming soon</p>
            </div>
            <div className="mt-6 flex flex-wrap gap-4 justify-center">
              <button className="px-4 py-2 bg-ocean text-white rounded-lg hover:bg-ocean/90">All Waterways</button>
              <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">Major Rivers</button>
              <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">Canal Networks</button>
              <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">Lakes & Lagoons</button>
            </div>
          </div>
        </div>
      </section>

      {/* Countries Grid */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Waterways by Country</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {countries.map((country, index) => (
              <motion.div
                key={country.name}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow"
              >
                <h3 className="text-xl font-semibold mb-2">{country.name}</h3>
                <p className="text-ocean font-medium mb-1">{country.waterways} navigable</p>
                <p className="text-gray-600 text-sm">{country.highlight}</p>
                <Link href={`/waterways/${country.name.toLowerCase().replace(' ', '-')}`} className="text-ocean hover:text-river font-medium text-sm mt-4 inline-block">
                  View Details →
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Major Rivers Section */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Major European Rivers</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg p-6">
              <h3 className="text-2xl font-semibold mb-4">Rhine</h3>
              <p className="text-gray-600 mb-4">
                Flowing 1,233 km from the Swiss Alps to the North Sea, the Rhine is one of Europe's most important waterways, 
                connecting Switzerland, Germany, France, and the Netherlands.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-700">
                  <span className="w-2 h-2 bg-ocean rounded-full mr-2"></span>
                  Major ports: Basel, Strasbourg, Cologne, Rotterdam
                </li>
                <li className="flex items-center text-gray-700">
                  <span className="w-2 h-2 bg-ocean rounded-full mr-2"></span>
                  UNESCO World Heritage Middle Rhine Valley
                </li>
              </ul>
            </div>
            
            <div className="bg-white rounded-lg p-6">
              <h3 className="text-2xl font-semibold mb-4">Danube</h3>
              <p className="text-gray-600 mb-4">
                Europe's second-longest river at 2,850 km, the Danube flows through 10 countries from Germany's Black Forest 
                to the Black Sea, making it the most international river in the world.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-700">
                  <span className="w-2 h-2 bg-river rounded-full mr-2"></span>
                  Major cities: Vienna, Budapest, Belgrade, Bucharest
                </li>
                <li className="flex items-center text-gray-700">
                  <span className="w-2 h-2 bg-river rounded-full mr-2"></span>
                  Connected to Rhine via Main-Danube Canal
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Resources Section */}
      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="bg-ocean text-white rounded-lg p-8 text-center">
            <h2 className="text-3xl font-bold mb-4">Planning Your Waterway Journey?</h2>
            <p className="text-xl mb-8 max-w-2xl mx-auto">
              Download our comprehensive waterway guides with detailed lock information, navigation tips, and mooring locations.
            </p>
            <Link href="/guides" className="bg-white text-ocean px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors inline-block">
              Access Navigation Guides
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  )
}