import Head from 'next/head'
import Layout from '@/components/Layout'
import { motion } from 'framer-motion'

export default function About() {
  return (
    <Layout>
      <Head>
        <title>About Atlas Fluvial - European Waterway Navigation</title>
        <meta name="description" content="Learn about Atlas Fluvial and our mission to make European waterway navigation accessible to everyone." />
      </Head>

      <section className="bg-gradient-to-r from-atlas-dark to-ocean text-white py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-4xl font-bold mb-4">About Atlas Fluvial</h1>
            <p className="text-xl max-w-3xl">
              Empowering waterway travelers with comprehensive navigation resources since 2025.
            </p>
          </motion.div>
        </div>
      </section>

      <section className="py-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="prose prose-lg"
            >
              <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
              <p className="text-gray-600 mb-6">
                Atlas Fluvial was founded with a simple yet ambitious goal: to make European waterway navigation 
                accessible, safe, and enjoyable for everyone. We believe that the freedom of exploring Europe's 
                vast network of canals and rivers should be available to all who dream of it.
              </p>
              
              <h3 className="text-2xl font-semibold mb-4">What We Provide</h3>
              <p className="text-gray-600 mb-6">
                Our comprehensive navigation guides, interactive maps, and planning tools are the result of 
                decades of collective experience navigating European waterways. We combine traditional navigation 
                wisdom with modern technology to provide you with the most accurate and up-to-date information available.
              </p>

              <h3 className="text-2xl font-semibold mb-4">Our Expertise</h3>
              <p className="text-gray-600 mb-6">
                Our team consists of experienced navigators, cartographers, and waterway enthusiasts who have 
                personally traveled thousands of kilometers across European waterways. This firsthand experience 
                ensures that our guides contain not just technical information, but practical insights that can 
                only come from real-world navigation.
              </p>

              <div className="bg-ocean/10 rounded-lg p-6 my-8">
                <h3 className="text-xl font-semibold mb-3">Our Values</h3>
                <ul className="space-y-2">
                  <li className="flex items-start">
                    <span className="text-ocean mr-2">•</span>
                    <span><strong>Accuracy:</strong> Every detail verified and regularly updated</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-ocean mr-2">•</span>
                    <span><strong>Accessibility:</strong> Information presented clearly for all experience levels</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-ocean mr-2">•</span>
                    <span><strong>Sustainability:</strong> Promoting responsible waterway tourism</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-ocean mr-2">•</span>
                    <span><strong>Community:</strong> Building connections among waterway travelers</span>
                  </li>
                </ul>
              </div>

              <h3 className="text-2xl font-semibold mb-4">Looking Forward</h3>
              <p className="text-gray-600 mb-6">
                As we continue to expand our coverage and enhance our tools, we remain committed to our core 
                mission: helping you discover the joy and freedom of European waterway travel. Whether you're 
                planning your first canal cruise or you're a seasoned navigator, Atlas Fluvial is here to 
                support your journey.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-12 bg-gray-50 rounded-lg p-8 text-center"
            >
              <h3 className="text-2xl font-bold mb-4">Start Your Journey Today</h3>
              <p className="text-gray-600 mb-6">
                Join thousands of waterway travelers who trust Atlas Fluvial for their navigation needs.
              </p>
              <a href="mailto:info@atlasfluvial.com" className="bg-ocean text-white px-8 py-3 rounded-lg font-semibold hover:bg-ocean/90 transition-colors inline-block">
                Contact Us
              </a>
            </motion.div>
          </div>
        </div>
      </section>
    </Layout>
  )
}