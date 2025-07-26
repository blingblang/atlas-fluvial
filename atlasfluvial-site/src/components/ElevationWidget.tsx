import React, { useState, useCallback } from 'react';
import { MapPinIcon, MagnifyingGlassIcon, ChartBarIcon } from '@heroicons/react/24/outline';

interface ElevationData {
  river_name?: string;
  elevation_m?: number;
  coordinates?: { lat: number; lon: number };
  segment_id?: string;
  distance_km?: number;
}

interface ElevationResponse {
  success: boolean;
  data?: {
    answer?: string;
    structured_data?: ElevationData | {
      nearest_river?: ElevationData;
      segments?: ElevationData[];
      profile?: Array<{
        distance_km: number;
        elevation_m: number;
        segment_id: string;
      }>;
    };
  };
  error?: string;
}

const ElevationWidget: React.FC = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ElevationResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'query' | 'river' | 'location'>('query');

  // Form states for structured queries
  const [riverName, setRiverName] = useState('');
  const [latitude, setLatitude] = useState('');
  const [longitude, setLongitude] = useState('');

  const API_BASE = process.env.NEXT_PUBLIC_ELEVATION_API || 'http://localhost:8000';

  const handleNaturalQuery = useCallback(async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/v1/elevation/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        error: 'Failed to connect to elevation service'
      });
    } finally {
      setLoading(false);
    }
  }, [query, API_BASE]);

  const handleRiverQuery = useCallback(async () => {
    if (!riverName.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/v1/elevation/river`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ river_name: riverName, country: 'FR' })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        error: 'Failed to connect to elevation service'
      });
    } finally {
      setLoading(false);
    }
  }, [riverName, API_BASE]);

  const handleLocationQuery = useCallback(async () => {
    const lat = parseFloat(latitude);
    const lon = parseFloat(longitude);

    if (isNaN(lat) || isNaN(lon)) {
      setResult({
        success: false,
        error: 'Please enter valid coordinates'
      });
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(`${API_BASE}/api/v1/elevation/coordinates`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          latitude: lat,
          longitude: lon,
          search_radius_km: 10
        })
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({
        success: false,
        error: 'Failed to connect to elevation service'
      });
    } finally {
      setLoading(false);
    }
  }, [latitude, longitude, API_BASE]);

  const renderResult = () => {
    if (!result) return null;

    if (!result.success) {
      return (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-700">Error: {result.error}</p>
        </div>
      );
    }

    const { data } = result;
    if (!data) return null;

    // Natural language response
    if (data.answer) {
      return (
        <div className="mt-4 space-y-4">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <p className="text-gray-800">{data.answer}</p>
          </div>
          
          {data.structured_data && (
            <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h4 className="font-semibold mb-2">Structured Data:</h4>
              <pre className="text-sm overflow-x-auto">
                {JSON.stringify(data.structured_data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      );
    }

    // River query response
    if ('segments' in (data as any)) {
      const riverData = data as any;
      return (
        <div className="mt-4 space-y-4">
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h4 className="font-semibold mb-2">{riverData.river_name}</h4>
            <p>Segments: {riverData.segment_count}</p>
            <p>Elevation range: {riverData.min_elevation_m}m to {riverData.max_elevation_m}m ASL</p>
          </div>
          
          <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg max-h-64 overflow-y-auto">
            <h4 className="font-semibold mb-2">Segments:</h4>
            {riverData.segments.map((seg: any, idx: number) => (
              <div key={idx} className="mb-2 text-sm">
                <span className="font-medium">{seg.segment_id}:</span> {seg.elevation_m}m
                <span className="text-gray-500 ml-2">
                  ({seg.coordinates.lat.toFixed(4)}, {seg.coordinates.lon.toFixed(4)})
                </span>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // Coordinate query response
    if ('nearest_river' in (data as any)) {
      const locData = data as any;
      const river = locData.nearest_river;
      return (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h4 className="font-semibold mb-2">Nearest River: {river.river_name}</h4>
          <p>Segment: {river.segment_id}</p>
          <p>Elevation: {river.elevation_m}m ASL</p>
          <p>Distance: {river.distance_km}km away</p>
          <p className="text-sm text-gray-600 mt-2">
            River location: ({river.segment_coordinates.lat.toFixed(4)}, {river.segment_coordinates.lon.toFixed(4)})
          </p>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">River Elevation Finder</h2>
      
      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg">
        <button
          onClick={() => setActiveTab('query')}
          className={`flex-1 py-2 px-4 rounded-md transition-colors ${
            activeTab === 'query'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          <MagnifyingGlassIcon className="w-5 h-5 inline mr-2" />
          Natural Query
        </button>
        <button
          onClick={() => setActiveTab('river')}
          className={`flex-1 py-2 px-4 rounded-md transition-colors ${
            activeTab === 'river'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          <ChartBarIcon className="w-5 h-5 inline mr-2" />
          By River
        </button>
        <button
          onClick={() => setActiveTab('location')}
          className={`flex-1 py-2 px-4 rounded-md transition-colors ${
            activeTab === 'location'
              ? 'bg-white text-blue-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          <MapPinIcon className="w-5 h-5 inline mr-2" />
          By Location
        </button>
      </div>

      {/* Query Forms */}
      {activeTab === 'query' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Ask about river elevations
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleNaturalQuery()}
              placeholder="e.g., What is the elevation of the Seine in Paris?"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleNaturalQuery}
            disabled={loading || !query.trim()}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      )}

      {activeTab === 'river' && (
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              River Name
            </label>
            <input
              type="text"
              value={riverName}
              onChange={(e) => setRiverName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleRiverQuery()}
              placeholder="e.g., Loire, Seine, Vilaine"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleRiverQuery}
            disabled={loading || !riverName.trim()}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Searching...' : 'Get Elevation Data'}
          </button>
        </div>
      )}

      {activeTab === 'location' && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Latitude
              </label>
              <input
                type="number"
                value={latitude}
                onChange={(e) => setLatitude(e.target.value)}
                placeholder="e.g., 47.2184"
                step="0.0001"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Longitude
              </label>
              <input
                type="number"
                value={longitude}
                onChange={(e) => setLongitude(e.target.value)}
                placeholder="e.g., -1.5536"
                step="0.0001"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <button
            onClick={handleLocationQuery}
            disabled={loading || !latitude || !longitude}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Searching...' : 'Find Nearest River'}
          </button>
        </div>
      )}

      {/* Results */}
      {renderResult()}

      {/* Example Queries */}
      {activeTab === 'query' && !result && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-semibold text-gray-700 mb-2">Example queries:</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            <li>• What is the elevation of the Loire at its source?</li>
            <li>• How high is the Seine in Paris?</li>
            <li>• Show me the elevation profile of the Vilaine river</li>
            <li>• Find elevation near Nantes</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ElevationWidget;