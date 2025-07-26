import { useState } from 'react'
import Link from 'next/link'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'
import ComingSoonModal from './ComingSoonModal'

const navigation = [
  { name: 'Home', href: '/' },
  { name: 'Waterways', href: '/waterways' },
  { name: 'Journey Planning', href: '/planning' },
  { name: 'Navigation Guides', href: '/guides' },
  { name: 'Vessel Options', href: '/vessels' },
  { name: 'Tools', href: '/tools', 
    submenu: [
      { name: 'AI Assistant', href: '/tools/waterways-assistant' },
      { name: 'Elevation Finder', href: '/tools/elevation' }
    ]
  },
  { name: 'Resources', href: '/resources' },
  { name: 'About', href: '/about' },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <div className="min-h-screen bg-atlas-light">
      <ComingSoonModal />
      
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <div className="flex items-center">
              <Link href="/" className="flex items-center">
                <span className="text-2xl font-bold text-ocean">Atlas Fluvial</span>
              </Link>
            </div>
            
            {/* Desktop navigation */}
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                {navigation.map((item) => (
                  item.submenu ? (
                    <div key={item.name} className="relative group">
                      <Link href={item.href} className="text-gray-700 hover:text-ocean px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center">
                        {item.name}
                        <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </Link>
                      <div className="absolute left-0 mt-2 w-48 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                        <div className="py-1">
                          {item.submenu.map((subitem) => (
                            <Link
                              key={subitem.name}
                              href={subitem.href}
                              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-ocean"
                            >
                              {subitem.name}
                            </Link>
                          ))}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <Link
                      key={item.name}
                      href={item.href}
                      className="text-gray-700 hover:text-ocean px-3 py-2 rounded-md text-sm font-medium transition-colors"
                    >
                      {item.name}
                    </Link>
                  )
                ))}
              </div>
            </div>
            
            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                type="button"
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-ocean hover:bg-gray-100"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                <span className="sr-only">Open main menu</span>
                {mobileMenuOpen ? (
                  <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                ) : (
                  <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {mobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigation.map((item) => (
                item.submenu ? (
                  <div key={item.name}>
                    <div className="text-gray-700 px-3 py-2 rounded-md text-base font-medium">
                      {item.name}
                    </div>
                    <div className="pl-6">
                      {item.submenu.map((subitem) => (
                        <Link
                          key={subitem.name}
                          href={subitem.href}
                          className="text-gray-600 hover:text-ocean block px-3 py-2 rounded-md text-sm"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          {subitem.name}
                        </Link>
                      ))}
                    </div>
                  </div>
                ) : (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="text-gray-700 hover:text-ocean block px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    {item.name}
                  </Link>
                )
              ))}
            </div>
          </div>
        )}
      </nav>

      {/* Main content */}
      <main>{children}</main>

      {/* Footer */}
      <footer className="bg-atlas-dark text-white mt-16">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-lg font-bold mb-4">Atlas Fluvial</h3>
              <p className="text-gray-300">Your comprehensive guide to navigating European waterways with confidence.</p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li><Link href="/waterways" className="text-gray-300 hover:text-white">Waterway Maps</Link></li>
                <li><Link href="/guides" className="text-gray-300 hover:text-white">Navigation Guides</Link></li>
                <li><Link href="/planning" className="text-gray-300 hover:text-white">Journey Planning</Link></li>
                <li><Link href="/tools/waterways-assistant" className="text-gray-300 hover:text-white">AI Assistant</Link></li>
                <li><Link href="/tools/elevation" className="text-gray-300 hover:text-white">Elevation Tool</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Contact</h4>
              <p className="text-gray-300">For inquiries about Atlas Fluvial:</p>
              <a href="mailto:info@atlasfluvial.com" className="text-river hover:text-canal mt-2 inline-block">
                info@atlasfluvial.com
              </a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-400">
            <p>&copy; {new Date().getFullYear()} Atlas Fluvial. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}