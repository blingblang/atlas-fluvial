import React, { useState, useRef, useEffect } from 'react';
import { 
  ChatBubbleLeftRightIcon, 
  MapIcon, 
  InformationCircleIcon,
  SparklesIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  confidence?: number;
  sources?: number;
  entities?: string[];
}

interface QueryResponse {
  success: boolean;
  question: string;
  answer?: string;
  confidence?: number;
  retrieved_info?: {
    sources: any[];
    tools_used: string[];
    entities_found: string[];
  };
  error?: string;
  processing_time_ms?: number;
}

const WaterwaysAssistant: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Hello! I\'m your French Waterways Assistant. I can help you with information about rivers, canals, navigation, locks, and more. What would you like to know?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showExamples, setShowExamples] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_BASE = process.env.NEXT_PUBLIC_RAG_API || 'http://localhost:8001';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setShowExamples(false);

    try {
      const response = await fetch(`${API_BASE}/api/v1/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: input,
          use_compression: true,
          include_sources: true
        })
      });

      const data: QueryResponse = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.answer || data.error || 'Sorry, I couldn\'t process that query.',
        timestamp: new Date(),
        confidence: data.confidence,
        sources: data.retrieved_info?.sources?.length,
        entities: data.retrieved_info?.entities_found
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I\'m having trouble connecting to the knowledge base. Please try again later.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setInput(example);
    setShowExamples(false);
  };

  const exampleQueries = [
    { icon: '📏', text: 'What is the elevation of the Canal du Midi near Toulouse?' },
    { icon: '🚢', text: 'Are there locks on the Rhône suitable for pleasure boats?' },
    { icon: '📍', text: 'Find waterways near Carcassonne' },
    { icon: '⚓', text: 'What is the maximum draft allowed on the Seine?' },
    { icon: '🗺️', text: 'How many locks between Lyon and the Mediterranean?' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-xl max-w-4xl mx-auto h-[600px] flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <ChatBubbleLeftRightIcon className="w-6 h-6" />
            <h2 className="text-xl font-semibold">French Waterways Assistant</h2>
            <span className="bg-blue-500 text-xs px-2 py-1 rounded-full flex items-center">
              <SparklesIcon className="w-3 h-3 mr-1" />
              RAG Enhanced
            </span>
          </div>
          <div className="flex items-center space-x-2 text-sm">
            <MapIcon className="w-4 h-4" />
            <span>Powered by RiverATLAS</span>
          </div>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-4 ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              
              {/* Metadata for assistant messages */}
              {message.type === 'assistant' && (message.confidence || message.sources) && (
                <div className="mt-2 pt-2 border-t border-gray-200 text-xs text-gray-600">
                  <div className="flex items-center space-x-3">
                    {message.confidence && (
                      <span className="flex items-center">
                        <div className="w-2 h-2 rounded-full bg-green-500 mr-1"></div>
                        {Math.round(message.confidence * 100)}% confident
                      </span>
                    )}
                    {message.sources && (
                      <span>{message.sources} sources</span>
                    )}
                  </div>
                  {message.entities && message.entities.length > 0 && (
                    <div className="mt-1 flex flex-wrap gap-1">
                      {message.entities.map((entity, idx) => (
                        <span key={idx} className="bg-gray-200 px-2 py-0.5 rounded text-xs">
                          {entity}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg p-4 flex items-center space-x-2">
              <ArrowPathIcon className="w-4 h-4 animate-spin text-blue-600" />
              <span className="text-sm text-gray-600">Searching knowledge base...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Examples */}
      {showExamples && messages.length === 1 && (
        <div className="p-4 border-t bg-gray-50">
          <p className="text-sm text-gray-600 mb-3 flex items-center">
            <InformationCircleIcon className="w-4 h-4 mr-1" />
            Try these example queries:
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {exampleQueries.map((example, idx) => (
              <button
                key={idx}
                onClick={() => handleExampleClick(example.text)}
                className="text-left p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-400 hover:bg-blue-50 transition-colors text-sm"
              >
                <span className="mr-2">{example.icon}</span>
                {example.text}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="p-4 border-t">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about French waterways, navigation, locks, elevations..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          This assistant uses RAG to provide accurate information from our comprehensive waterways database.
        </p>
      </form>
    </div>
  );
};

export default WaterwaysAssistant;