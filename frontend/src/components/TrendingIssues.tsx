'use client';

import { useState, useEffect } from 'react';
import { api, Issue } from '@/lib/api';

export default function TrendingIssues() {
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    loadTrending();
  }, []);

  const loadTrending = async () => {
    try {
      const data = await api.getTrending();
      setIssues(data);
    } catch (error) {
      console.error('Failed to load trending:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExpand = async (id: string) => {
    if (expandedId !== id) {
      setExpandedId(id);
      // Count view
      api.sendFeedback(id, 'view').catch(console.error);
    } else {
      setExpandedId(null);
    }
  };

  const handleUseful = async (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    try {
      await api.sendFeedback(id, 'useful');
      // Optimistic update
      setIssues(issues.map(i => 
        i.id === id ? { ...i, useful_count: (i.useful_count || 0) + 1 } : i
      ));
      alert('Thanks for your feedback!');
    } catch (error) {
      console.error('Feedback failed:', error);
    }
  };

  if (loading) return <div className="text-gray-500 text-center py-4">Loading trending knowledge...</div>;
  if (issues.length === 0) return null;

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">🔥 Trending Challenges</h2>
      <div className="grid gap-4">
        {issues.map((issue) => (
          <div 
            key={issue.id} 
            className={`border rounded-lg p-5 bg-white transition-all cursor-pointer ${
              expandedId === issue.id ? 'ring-2 ring-orange-400 shadow-lg' : 'hover:shadow-md border-l-4 border-l-orange-400'
            }`}
            onClick={() => handleExpand(issue.id)}
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-bold text-gray-900">{issue.title}</h3>
              <div className="flex gap-2 text-xs font-mono text-gray-500">
                <span title="Views">👀 {issue.view_count || 0}</span>
                <span title="Useful votes">👍 {issue.useful_count || 0}</span>
              </div>
            </div>
            
            <div className="prose prose-sm max-w-none text-gray-600">
              <p className={expandedId === issue.id ? 'mb-4' : 'line-clamp-2'}>
                {issue.content}
              </p>
              
              {expandedId === issue.id && (
                <div className="mt-4 pt-4 border-t border-gray-100 animate-fade-in">
                  <h4 className="font-bold text-green-700 mb-2">💡 Solution:</h4>
                  <div className="bg-green-50 p-4 rounded-md text-gray-800 whitespace-pre-wrap">
                    {issue.solution}
                  </div>
                  
                  <div className="mt-4 flex justify-end">
                    <button
                      onClick={(e) => handleUseful(e, issue.id)}
                      className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-full hover:bg-blue-100 transition-colors text-sm font-medium"
                    >
                      👍 This helped me!
                    </button>
                  </div>
                </div>
              )}
            </div>

            <div className="flex flex-wrap gap-2 mt-3">
              {issue.tags.map(tag => (
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
