'use client';

import { useState } from 'react';
import { api, IssueCreate } from '@/lib/api';

export default function IssueForm({ onSuccess }: { onSuccess?: () => void }) {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    solution: '',
    tags: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const issue: IssueCreate = {
        title: formData.title,
        content: formData.content,
        solution: formData.solution,
        tags: formData.tags.split(',').map(t => t.trim()).filter(Boolean),
        metadata: { source: 'web-ui' },
      };
      await api.createIssue(issue);
      setFormData({ title: '', content: '', solution: '', tags: '' });
      onSuccess?.();
    } catch (error) {
      console.error('Failed to create issue:', error);
      alert('Failed to create issue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-6 border rounded-lg shadow-sm bg-white">
      <h2 className="text-xl font-bold mb-4">Report New Challenge</h2>
      
      <div>
        <label className="block text-sm font-medium text-gray-700">Title</label>
        <input
          type="text"
          required
          className="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={formData.title}
          onChange={e => setFormData({ ...formData, title: e.target.value })}
          placeholder="e.g., Timeout Error in Production"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Content (The Challenge)</label>
        <textarea
          required
          rows={4}
          className="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={formData.content}
          onChange={e => setFormData({ ...formData, content: e.target.value })}
          placeholder="Describe the error, logs, and context..."
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Solution (The Fix)</label>
        <textarea
          required
          rows={4}
          className="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={formData.solution}
          onChange={e => setFormData({ ...formData, solution: e.target.value })}
          placeholder="How did you fix it? What was the reasoning?"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Tags (comma separated)</label>
        <input
          type="text"
          className="mt-1 block w-full rounded-md border border-gray-300 p-2 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={formData.tags}
          onChange={e => setFormData({ ...formData, tags: e.target.value })}
          placeholder="python, timeout, network"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
      >
        {loading ? 'Saving...' : 'Save Knowledge'}
      </button>
    </form>
  );
}
