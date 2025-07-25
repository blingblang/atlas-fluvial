# Atlas Fluvial

A modern web application for European waterway navigation, built with Next.js and deployed on Netlify.

🌐 **Live Site**: https://atlas-fluvial.netlify.app

## Overview

Atlas Fluvial is a comprehensive guide to European waterways, providing:
- Interactive waterway maps covering 19 countries
- Detailed navigation guides with lock information
- Journey planning tools
- Vessel charter and purchase resources
- Real-time weather and water level data

## Technology Stack

- **Framework**: Next.js 14 with TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **UI Components**: Headless UI
- **Deployment**: Netlify

## Project Structure

```
atlasfluvial-site/
├── src/
│   ├── pages/          # Next.js pages
│   ├── components/     # React components
│   └── styles/         # Global styles
├── public/             # Static assets
├── .env.local         # Environment variables
└── netlify.toml       # Netlify configuration
```

## Key Features

### Coming Soon Gate
The site features a configurable "coming soon" popup that can be controlled via environment variables:
- Set `NEXT_PUBLIC_GATE_OPEN=true` to open the site
- Set `NEXT_PUBLIC_GATE_OPEN=false` to show the coming soon popup

### Pages
- **Home**: Overview of services and features
- **Waterways**: Interactive maps and country-specific information
- **Journey Planning**: Route planning tools and calculators
- **Navigation Guides**: Professional-grade navigation resources
- **Vessel Options**: Charter, purchase, and import information
- **Resources**: Weather, regulations, and emergency contacts
- **About**: Mission and company information

## Development

### Prerequisites
- Node.js 18+
- npm or yarn

### Setup
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
npm run export
```

### Environment Variables
Copy `.env.local.example` to `.env.local` and configure:
```
NEXT_PUBLIC_GATE_OPEN=false  # Set to true to open the site
```

## Deployment

The site is configured for static export and deployment to Netlify:

```bash
# Build and export
npm run build && npm run export

# Deploy to Netlify (requires Netlify CLI)
netlify deploy --prod --dir=out
```

## Content Strategy

All content has been completely rewritten to:
- Focus on empowering independent waterway travel
- Provide practical, actionable information
- Use clear, accessible language
- Emphasize safety and preparation

## Design Philosophy

The design emphasizes:
- Clean, modern aesthetics
- Easy navigation
- Mobile responsiveness
- Fast loading times
- Accessibility

## Future Enhancements

- Interactive waterway route planner
- Real-time vessel tracking
- Community forums
- Mobile applications
- Multi-language support

## License

© 2025 Atlas Fluvial. All rights reserved.