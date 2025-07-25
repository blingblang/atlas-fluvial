import { Fragment, useEffect, useState } from 'react'
import { Dialog, Transition } from '@headlessui/react'
import { motion } from 'framer-motion'

export default function ComingSoonModal() {
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    // Check if gate should be open from environment variable
    const gateOpen = process.env.NEXT_PUBLIC_GATE_OPEN === 'true'
    
    if (!gateOpen) {
      setIsOpen(true)
    }
  }, [])

  if (process.env.NEXT_PUBLIC_GATE_OPEN === 'true') {
    return null
  }

  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={() => {}}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-900 bg-opacity-75 backdrop-blur-md transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-ocean/10">
                    <svg className="h-12 w-12 text-ocean" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" />
                    </svg>
                  </div>
                  <div className="mt-5 text-center">
                    <Dialog.Title as="h3" className="text-2xl font-bold leading-6 text-gray-900">
                      Atlas Fluvial
                    </Dialog.Title>
                    <div className="mt-4">
                      <p className="text-lg text-gray-600">
                        Charting New Waters
                      </p>
                      <p className="mt-4 text-base text-gray-500">
                        Our comprehensive guide to European waterways is currently being developed.
                      </p>
                      <p className="mt-2 text-base text-gray-500">
                        Navigate back soon for the complete experience.
                      </p>
                    </div>
                  </div>
                  <div className="mt-8">
                    <motion.div
                      className="rounded-md bg-ocean px-4 py-2 text-center text-sm font-semibold text-white shadow-sm"
                      animate={{
                        scale: [1, 1.05, 1],
                      }}
                      transition={{
                        duration: 2,
                        repeat: Infinity,
                        repeatType: "reverse",
                      }}
                    >
                      Coming Soon
                    </motion.div>
                  </div>
                </motion.div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  )
}