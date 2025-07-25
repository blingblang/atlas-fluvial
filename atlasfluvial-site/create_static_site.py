"""Create a static version of the Atlas Fluvial site."""

import os
import json
import shutil
from pathlib import Path

def create_static_site():
    """Create static HTML files from the Next.js components."""
    
    # Create output directory
    out_dir = Path("out")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir()
    
    # Copy public files
    public_dir = Path("public")
    if public_dir.exists():
        for item in public_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, out_dir)
    
    # Copy the France map if it exists
    france_map = Path("out/france-map-grayscale.jpg")
    if france_map.exists():
        shutil.copy2(france_map, out_dir)
    
    # Base HTML template
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Atlas Fluvial</title>
    <meta name="description" content="{description}">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Merriweather:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1a202c;
            background: #f7fafc;
        }}
        .nav {{
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 50;
        }}
        .nav-container {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #0064C8;
            text-decoration: none;
        }}
        .nav-links {{
            display: flex;
            gap: 2rem;
            list-style: none;
        }}
        .nav-links a {{
            color: #4a5568;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}
        .nav-links a:hover {{
            color: #0064C8;
        }}
        .hero {{
            background: linear-gradient(135deg, #0064C8 0%, #0078DC 100%);
            color: white;
            padding: 6rem 2rem;
            text-align: center;
        }}
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }}
        .hero p {{
            font-size: 1.25rem;
            max-width: 800px;
            margin: 0 auto 2rem;
            opacity: 0.9;
        }}
        .button-group {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .button {{
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s;
            display: inline-block;
        }}
        .button-primary {{
            background: white;
            color: #0064C8;
        }}
        .button-primary:hover {{
            background: #f7fafc;
            transform: translateY(-2px);
        }}
        .button-secondary {{
            border: 2px solid white;
            color: white;
        }}
        .button-secondary:hover {{
            background: white;
            color: #0064C8;
        }}
        .section {{
            padding: 4rem 2rem;
            max-width: 1280px;
            margin: 0 auto;
        }}
        .section-title {{
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 3rem;
        }}
        .grid {{
            display: grid;
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        .grid-3 {{
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        }}
        .card {{
            background: white;
            padding: 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: box-shadow 0.2s;
        }}
        .card:hover {{
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .card h3 {{
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: #1a202c;
        }}
        .card p {{
            color: #718096;
            line-height: 1.6;
        }}
        .footer {{
            background: #1a202c;
            color: white;
            padding: 3rem 2rem;
            margin-top: 4rem;
        }}
        .footer-container {{
            max-width: 1280px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
        }}
        .footer h3 {{
            margin-bottom: 1rem;
        }}
        .footer a {{
            color: #cbd5e0;
            text-decoration: none;
        }}
        .footer a:hover {{
            color: white;
        }}
        .footer-bottom {{
            text-align: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #2d3748;
            color: #a0aec0;
        }}
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            .hero h1 {{
                font-size: 2rem;
            }}
            .button-group {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-container">
            <a href="/" class="logo">Atlas Fluvial</a>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="/waterways/">Waterways</a></li>
                <li><a href="/planning/">Journey Planning</a></li>
                <li><a href="/guides/">Navigation Guides</a></li>
                <li><a href="/vessels/">Vessel Options</a></li>
                <li><a href="/resources/">Resources</a></li>
                <li><a href="/about/">About</a></li>
            </ul>
        </div>
    </nav>
    
    {content}
    
    <footer class="footer">
        <div class="footer-container">
            <div>
                <h3>Atlas Fluvial</h3>
                <p>Your comprehensive guide to navigating European waterways with confidence.</p>
            </div>
            <div>
                <h3>Quick Links</h3>
                <ul style="list-style: none; padding: 0;">
                    <li><a href="/waterways/">Waterway Maps</a></li>
                    <li><a href="/guides/">Navigation Guides</a></li>
                    <li><a href="/planning/">Journey Planning</a></li>
                </ul>
            </div>
            <div>
                <h3>Contact</h3>
                <p>For inquiries about Atlas Fluvial:</p>
                <a href="mailto:info@atlasfluvial.com">info@atlasfluvial.com</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 Atlas Fluvial. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
    
    # Define pages and their content
    pages = {
        "index.html": {
            "title": "Navigate European Waterways",
            "description": "Your comprehensive guide to exploring Europe's canals, rivers, and waterways. Plan your journey with confidence using our detailed navigation guides and resources.",
            "content": """
    <section class="hero">
        <h1>Navigate Europe's Waterways</h1>
        <p>Discover the freedom of exploring Europe's intricate network of canals and rivers at your own pace.</p>
        <div class="button-group">
            <a href="/waterways/" class="button button-primary">Explore Waterways</a>
            <a href="/planning/" class="button button-secondary">Plan Your Journey</a>
        </div>
    </section>
    
    <section class="section">
        <h2 class="section-title">Your Complete Navigation Resource</h2>
        <p style="text-align: center; color: #718096; max-width: 800px; margin: 0 auto 3rem;">
            Whether you're planning your first canal journey or you're an experienced navigator, Atlas Fluvial provides everything you need.
        </p>
        
        <div class="grid grid-3">
            <div class="card">
                <h3>Detailed Waterway Maps</h3>
                <p>Interactive maps covering over 40,000 kilometers of navigable waterways across 19 European countries.</p>
            </div>
            <div class="card">
                <h3>Navigation Guides</h3>
                <p>Comprehensive guides with lock information, mooring locations, and essential navigation details for safe passage.</p>
            </div>
            <div class="card">
                <h3>Vessel Information</h3>
                <p>Everything you need to know about chartering, purchasing, or bringing your own vessel to European waterways.</p>
            </div>
        </div>
    </section>"""
        },
        
        "waterways/index.html": {
            "title": "European Waterways",
            "description": "Explore navigable waterways across 19 European countries. Detailed maps and information for canals, rivers, and lakes.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>European Waterways</h1>
        <p>Over 40,000 kilometers of navigable waterways connecting cities, towns, and countryside across Europe.</p>
    </section>
    
    <section class="section">
        <h2 class="section-title">Waterways by Country</h2>
        <div class="grid grid-3">
            <a href="/waterways/france/" class="card" style="text-decoration: none; color: inherit; display: block;">
                <h3>France</h3>
                <p style="color: #0064C8; font-weight: 600;">8,500 km navigable</p>
                <p>Canal du Midi, Seine, Rhône</p>
            </a>
            <div class="card">
                <h3>Netherlands</h3>
                <p style="color: #0064C8; font-weight: 600;">6,200 km navigable</p>
                <p>Amsterdam Canals, IJsselmeer</p>
            </div>
            <div class="card">
                <h3>Germany</h3>
                <p style="color: #0064C8; font-weight: 600;">7,300 km navigable</p>
                <p>Rhine, Main-Danube Canal</p>
            </div>
            <div class="card">
                <h3>Belgium</h3>
                <p style="color: #0064C8; font-weight: 600;">2,000 km navigable</p>
                <p>Albert Canal, Meuse</p>
            </div>
            <div class="card">
                <h3>United Kingdom</h3>
                <p style="color: #0064C8; font-weight: 600;">3,200 km navigable</p>
                <p>Thames, Grand Union Canal</p>
            </div>
            <div class="card">
                <h3>Italy</h3>
                <p style="color: #0064C8; font-weight: 600;">2,400 km navigable</p>
                <p>Po River, Venetian Lagoon</p>
            </div>
        </div>
    </section>"""
        },
        
        "planning/index.html": {
            "title": "Journey Planning",
            "description": "Plan your perfect waterway journey with our comprehensive planning tools and expert advice.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>Journey Planning</h1>
        <p>Transform your waterway dreams into reality with our comprehensive planning resources.</p>
    </section>
    
    <section class="section">
        <div class="grid grid-3">
            <div class="card">
                <h3>Route Planning</h3>
                <p>Design your perfect itinerary with our route planning tools. Calculate distances, lock counts, and estimated journey times.</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>Interactive route builder</li>
                    <li>Distance calculations</li>
                    <li>Lock and bridge information</li>
                    <li>Fuel stop locations</li>
                </ul>
            </div>
            <div class="card">
                <h3>Seasonal Considerations</h3>
                <p>Navigate year-round with confidence. Understanding seasonal variations in water levels, weather, and operating hours.</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>Best travel seasons by region</li>
                    <li>Water level monitoring</li>
                    <li>Winter closures</li>
                    <li>Festival calendars</li>
                </ul>
            </div>
            <div class="card">
                <h3>Essential Preparation</h3>
                <p>Ensure smooth sailing with our comprehensive preparation checklists and requirement guides.</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>License requirements</li>
                    <li>Equipment checklists</li>
                    <li>Documentation needs</li>
                    <li>Safety protocols</li>
                </ul>
            </div>
        </div>
    </section>"""
        },
        
        "guides/index.html": {
            "title": "Navigation Guides",
            "description": "Professional navigation guides for European waterways. Detailed charts, lock information, and essential cruising data.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>Navigation Guides</h1>
        <p>Professional-grade navigation resources trusted by thousands of waterway travelers across Europe.</p>
    </section>
    
    <section class="section">
        <h2 class="section-title">2025 Edition Guides</h2>
        <p style="text-align: center; color: #718096; max-width: 800px; margin: 0 auto 3rem;">
            Updated annually with the latest navigation information, infrastructure changes, and regulatory updates.
        </p>
        
        <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h3>French Waterways Navigator</h3>
                        <p style="color: #0064C8; font-weight: 600;">2025 Edition</p>
                    </div>
                    <span style="font-size: 1.5rem; font-weight: bold;">€89</span>
                </div>
                <p>Complete coverage of 8,500km of French canals and rivers</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>480 pages</li>
                    <li>Full-color maps</li>
                    <li>Lock details</li>
                    <li>Mooring guides</li>
                </ul>
            </div>
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h3>Rhine & Moselle Guide</h3>
                        <p style="color: #0064C8; font-weight: 600;">2025 Edition</p>
                    </div>
                    <span style="font-size: 1.5rem; font-weight: bold;">€79</span>
                </div>
                <p>Comprehensive guide from Basel to Rotterdam</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>320 pages</li>
                    <li>Navigation charts</li>
                    <li>Port information</li>
                    <li>Cultural insights</li>
                </ul>
            </div>
        </div>
    </section>"""
        },
        
        "vessels/index.html": {
            "title": "Vessel Options",
            "description": "Explore vessel options for European waterway travel - charter, purchase, or bring your own boat.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>Vessel Options</h1>
        <p>Find the perfect vessel for your European waterway adventure.</p>
    </section>
    
    <section class="section">
        <div class="grid grid-3">
            <div class="card">
                <h2>Charter a Vessel</h2>
                <p>Perfect for first-time navigators or those seeking a hassle-free experience. Choose from hundreds of well-maintained vessels across Europe.</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>No license required options</li>
                    <li>Full briefing and support</li>
                    <li>Insurance included</li>
                </ul>
            </div>
            <div class="card">
                <h2>Buy a Vessel</h2>
                <p>Make your waterway dreams permanent with vessel ownership. Access our network of trusted brokers and marine surveyors.</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>New and used vessels</li>
                    <li>Purchase guidance</li>
                    <li>Mooring arrangements</li>
                </ul>
            </div>
            <div class="card">
                <h2>Bring Your Vessel</h2>
                <p>Navigate European waterways with your own vessel. We provide all the information needed for international cruising.</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>Transport logistics</li>
                    <li>Documentation requirements</li>
                    <li>Technical standards</li>
                </ul>
            </div>
        </div>
    </section>"""
        },
        
        "resources/index.html": {
            "title": "Resources",
            "description": "Essential resources for European waterway navigation - weather, regulations, emergency contacts, and more.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>Navigation Resources</h1>
        <p>Essential tools and information for safe and successful waterway navigation.</p>
    </section>
    
    <section class="section">
        <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));">
            <div class="card">
                <h2>Weather & Water Levels</h2>
                <p>Stay informed with real-time weather conditions and water level monitoring across European waterways.</p>
                <ul style="margin-top: 1rem; list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.5rem;">
                        <a href="#" style="color: #0064C8; font-weight: 500;">European Weather Service →</a>
                        <p style="font-size: 0.875rem; color: #718096;">Multi-day forecasts for all regions</p>
                    </li>
                    <li style="margin-bottom: 0.5rem;">
                        <a href="#" style="color: #0064C8; font-weight: 500;">Water Level Monitoring →</a>
                        <p style="font-size: 0.875rem; color: #718096;">Real-time gauge readings</p>
                    </li>
                </ul>
            </div>
            <div class="card">
                <h2>Regulations & Documentation</h2>
                <p>Comprehensive guides to international waterway regulations and required documentation.</p>
                <ul style="margin-top: 1rem; list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.5rem;">
                        <a href="#" style="color: #0064C8; font-weight: 500;">License Requirements →</a>
                        <p style="font-size: 0.875rem; color: #718096;">Country-specific boating licenses</p>
                    </li>
                    <li style="margin-bottom: 0.5rem;">
                        <a href="#" style="color: #0064C8; font-weight: 500;">Insurance Guidelines →</a>
                        <p style="font-size: 0.875rem; color: #718096;">Coverage requirements by country</p>
                    </li>
                </ul>
            </div>
        </div>
        
        <div class="card" style="margin-top: 2rem; background: #fee;">
            <h2 style="color: #c53030;">Emergency Contacts</h2>
            <div class="grid grid-3" style="margin-top: 1rem;">
                <div>
                    <h3>General Emergency</h3>
                    <p style="font-size: 2rem; font-weight: bold; color: #c53030;">112</p>
                    <p style="font-size: 0.875rem;">Valid in all EU countries</p>
                </div>
                <div>
                    <h3>Water Police</h3>
                    <p>Country-specific</p>
                    <a href="#" style="color: #0064C8;">View directory →</a>
                </div>
                <div>
                    <h3>Canal Authorities</h3>
                    <p>VHF Channel 10</p>
                    <p style="font-size: 0.875rem;">Standard in most regions</p>
                </div>
            </div>
        </div>
    </section>"""
        },
        
        "waterways/france/index.html": {
            "title": "France Waterways",
            "description": "Navigate France's extensive network of canals and rivers. Interactive map with detailed regional guides.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>France Waterways</h1>
        <p>8,500 kilometers of navigable waterways connecting the Atlantic, Mediterranean, and North Sea.</p>
    </section>
    
    <section class="section">
        <h2 class="section-title">Interactive Waterway Map</h2>
        <div style="position: relative; max-width: 1000px; margin: 0 auto;">
            <!-- France Map Container -->
            <div style="background: #f0f0f0; border-radius: 0.5rem; overflow: hidden; position: relative;">
                <img src="/france-map-grayscale.jpg" alt="France Waterways Map" style="width: 100%; height: auto; display: block; filter: grayscale(100%);">
                
                <!-- Nantes Clickable Overlay -->
                <a href="/maps/map_1_latest.pdf" 
                   style="position: absolute; left: 28.5%; top: 40%; width: 40px; height: 40px; display: block;"
                   title="Nantes and its environs">
                    <div style="position: relative; width: 100%; height: 100%;">
                        <!-- Pulsing dot -->
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 12px; height: 12px; background: #0064C8; border-radius: 50%; z-index: 2;"></div>
                        <!-- Pulsing ring animation -->
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 30px; height: 30px; border: 2px solid #0064C8; border-radius: 50%; animation: pulse 2s infinite; opacity: 0.6;"></div>
                        <!-- Tooltip on hover -->
                        <div style="position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); margin-bottom: 10px; padding: 0.5rem 1rem; background: #1a202c; color: white; border-radius: 0.25rem; white-space: nowrap; opacity: 0; visibility: hidden; transition: all 0.2s; pointer-events: none;">
                            Nantes and its environs
                            <div style="position: absolute; top: 100%; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-top: 6px solid #1a202c;"></div>
                        </div>
                    </div>
                </a>
            </div>
            
            <!-- Map Legend -->
            <div style="margin-top: 2rem; padding: 1.5rem; background: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h3 style="margin-bottom: 1rem;">Map Legend</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 12px; height: 12px; background: #0064C8; border-radius: 50%;"></div>
                        <span>Detailed Regional Maps Available</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 40px; height: 3px; background: #0064C8;"></div>
                        <span>Major Waterways</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 40px; height: 2px; background: #87CEEB;"></div>
                        <span>Secondary Waterways</span>
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            @keyframes pulse {
                0% {
                    transform: translate(-50%, -50%) scale(0.8);
                    opacity: 0.8;
                }
                50% {
                    transform: translate(-50%, -50%) scale(1.5);
                    opacity: 0.3;
                }
                100% {
                    transform: translate(-50%, -50%) scale(2);
                    opacity: 0;
                }
            }
            
            /* Show tooltip on hover */
            a[title]:hover > div > div:last-child {
                opacity: 1 !important;
                visibility: visible !important;
            }
        </style>
    </section>
    
    <section class="section">
        <h2 class="section-title">Major French Waterways</h2>
        <div class="grid grid-3">
            <div class="card">
                <h3>Canal du Midi</h3>
                <p>UNESCO World Heritage site connecting the Atlantic to the Mediterranean</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>240 km length</li>
                    <li>91 locks</li>
                    <li>Toulouse to Sète</li>
                </ul>
            </div>
            <div class="card">
                <h3>Seine River</h3>
                <p>France's second-longest river, navigable from Paris to the sea</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>777 km total</li>
                    <li>560 km navigable</li>
                    <li>Paris to Le Havre</li>
                </ul>
            </div>
            <div class="card">
                <h3>Rhône River</h3>
                <p>Major commercial waterway connecting Lyon to the Mediterranean</p>
                <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #718096;">
                    <li>812 km total</li>
                    <li>14 large locks</li>
                    <li>Lyon to Mediterranean</li>
                </ul>
            </div>
        </div>
    </section>"""
        },
        
        "about/index.html": {
            "title": "About Atlas Fluvial",
            "description": "Learn about Atlas Fluvial and our mission to make European waterway navigation accessible to everyone.",
            "content": """
    <section class="hero" style="padding: 4rem 2rem;">
        <h1>About Atlas Fluvial</h1>
        <p>Empowering waterway travelers with comprehensive navigation resources since 2025.</p>
    </section>
    
    <section class="section">
        <div style="max-width: 800px; margin: 0 auto;">
            <h2 style="font-size: 2rem; margin-bottom: 1.5rem;">Our Mission</h2>
            <p style="color: #718096; margin-bottom: 2rem; line-height: 1.8;">
                Atlas Fluvial was founded with a simple yet ambitious goal: to make European waterway navigation 
                accessible, safe, and enjoyable for everyone. We believe that the freedom of exploring Europe's 
                vast network of canals and rivers should be available to all who dream of it.
            </p>
            
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">What We Provide</h3>
            <p style="color: #718096; margin-bottom: 2rem; line-height: 1.8;">
                Our comprehensive navigation guides, interactive maps, and planning tools are the result of 
                decades of collective experience navigating European waterways. We combine traditional navigation 
                wisdom with modern technology to provide you with the most accurate and up-to-date information available.
            </p>
            
            <div class="card" style="background: #e6f3ff; margin: 2rem 0;">
                <h3 style="margin-bottom: 1rem;">Our Values</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.5rem;">• <strong>Accuracy:</strong> Every detail verified and regularly updated</li>
                    <li style="margin-bottom: 0.5rem;">• <strong>Accessibility:</strong> Information presented clearly for all experience levels</li>
                    <li style="margin-bottom: 0.5rem;">• <strong>Sustainability:</strong> Promoting responsible waterway tourism</li>
                    <li>• <strong>Community:</strong> Building connections among waterway travelers</li>
                </ul>
            </div>
            
            <div style="text-align: center; margin-top: 3rem;">
                <h3 style="margin-bottom: 1rem;">Start Your Journey Today</h3>
                <p style="color: #718096; margin-bottom: 1.5rem;">
                    Join thousands of waterway travelers who trust Atlas Fluvial for their navigation needs.
                </p>
                <a href="mailto:info@atlasfluvial.com" class="button button-primary" style="background: #0064C8; color: white;">
                    Contact Us
                </a>
            </div>
        </div>
    </section>"""
        }
    }
    
    # Create pages
    for page_path, page_data in pages.items():
        page_content = base_template.format(
            title=page_data["title"],
            description=page_data["description"],
            content=page_data["content"]
        )
        
        # Create directory if needed
        page_file = out_dir / page_path
        page_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(page_file, "w", encoding="utf-8") as f:
            f.write(page_content)
    
    # Create _redirects for Netlify
    redirects = """/*    /index.html    200"""
    with open(out_dir / "_redirects", "w") as f:
        f.write(redirects)
    
    print(f"Created static site in {out_dir}")
    return str(out_dir)

if __name__ == "__main__":
    create_static_site()