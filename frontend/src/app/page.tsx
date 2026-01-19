'use client';

import { useState } from 'react';
import TrendingIssues from '@/components/TrendingIssues';
import IssueForm from '@/components/IssueForm';
import SearchIssue from '@/components/SearchIssue';

export default function Home() {
  const [showAddForm, setShowAddForm] = useState(false);

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b shadow-sm sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">FixFlow</h1>
            <span className="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full font-medium">MVP</span>
          </div>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
          >
            {showAddForm ? 'Cancel' : '+ New Issue'}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 gap-8">
          
          {/* Add Form Section (Conditional) */}
          {showAddForm && (
            <div className="animate-fade-in-down">
              <IssueForm onSuccess={() => setShowAddForm(false)} />
            </div>
          )}

          {/* Search Section */}
          <section>
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-2">Semantic Search</h2>
              <p className="text-gray-600">Find solutions by describing the problem in natural language.</p>
            </div>
            <SearchIssue />
          </section>

          {/* Trending Section */}
          <section>
            <TrendingIssues />
          </section>

        </div>
      </div>
    </main>
  );
}
