'use client';

import { useState } from 'react';
import { api, SearchResult } from '@/lib/api';

export default function SearchIssue() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setExpandedId(null);
    try {
      const data = await api.searchIssues(query);
      setResults(data);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExpand = (id: string) => {
    if (expandedId !== id) {
      setExpandedId(id);
      api.sendFeedback(id, 'view').catch(console.error);
    } else {
      setExpandedId(null);
    }
  };

  const handleUseful = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await api.sendFeedback(id, 'useful');
      setResults(results.map(r => 
        r.id === id ? { ...r, useful_count: (r.useful_count || 0) + 1 } : r
      ));
      alert('Thanks for your feedback!');
    } catch (error) {
      console.error('Feedback failed:', error);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          className="flex-1 rounded-md border border-gray-300 p-3 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          placeholder="Describe your problem (e.g., 'React hydration error with dates')"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-gray-900 text-white px-6 py-2 rounded-md hover:bg-gray-800 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      <div className="space-y-4">
        {results.length === 0 && query && !loading && (
          <p className="text-gray-500 text-center py-4">No results found. Try a different description.</p>
        )}
        
        {results.map((result) => (
          <div 
            key={result.id} 
            className={`border rounded-lg p-5 bg-white transition-all cursor-pointer ${
              expandedId === result.id ? 'ring-2 ring-blue-500 shadow-lg' : 'hover:shadow-md'
            }`}
            onClick={() => handleExpand(result.id)}
          >
            <div className="flex justify-between items-start mb-2">
              <div className="flex flex-col">
                <h3 className="text-lg font-semibold text-blue-600">{result.title}</h3>
                <div className="flex gap-2 text-xs text-gray-400 mt-1">
                  <span>👀 {result.view_count || 0}</span>
                  <span>👍 {result.useful_count || 0}</span>
                </div>
              </div>
              <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full shrink-0 ml-2">
                Match: {(result.score * 100).toFixed(0)}%
              </span>
            </div>
            
            <div className="prose prose-sm max-w-none text-gray-600">
              <p className={expandedId === result.id ? 'mb-4' : 'line-clamp-2'}>
                {result.content}
              </p>
              
              {expandedId === result.id && (
                <div className="mt-4 pt-4 border-t border-gray-100 animate-fade-in">
                  <h4 className="font-bold text-gray-900 mb-2">💡 Solution:</h4>
                  <div className="bg-gray-50 p-4 rounded-md text-gray-800 whitespace-pre-wrap">
                    {result.solution}
                  </div>
                  <div className="mt-4 flex justify-end">
                    <button
                      onClick={(e) => handleUseful(e, result.id)}
                      className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition-colors text-xs font-medium"
                    >
                      👍 Helpful
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="flex flex-wrap gap-2 mt-3">
              {result.tags.map(tag => (
                <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
