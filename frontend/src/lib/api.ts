// Types matching Backend Pydantic models

export interface Issue {
  id: string;
  title: string;
  content: string;
  solution: string;
  tags: string[];
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  view_count: number;
  useful_count: number;
}

export interface IssueCreate {
  title: string;
  content: string;
  solution: string;
  tags: string[];
  metadata: Record<string, unknown>;
}

export interface SearchResult extends Issue {
  score: number;
}

export interface SearchQuery {
  query: string;
  limit?: number;
  filters?: Record<string, unknown>;
}

// API Client
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

async function fetchWithTimeout(resource: string, options: RequestInit & { timeout?: number } = {}) {
  const { timeout = 10000, ...fetchOptions } = options;
  
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  
  try {
    const response = await fetch(resource, {
      ...fetchOptions,
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  } catch (error: any) {
    clearTimeout(id);
    if (error.name === 'AbortError') {
      throw new Error(`Request timed out after ${timeout}ms`);
    }
    throw error;
  }
}

export const api = {
  async createIssue(issue: IssueCreate): Promise<Issue> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/issues`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(issue),
    });
    if (!response.ok) throw new Error('Failed to create issue');
    return response.json();
  },

  async searchIssues(query: string): Promise<SearchResult[]> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, limit: 5 }),
    });
    if (!response.ok) throw new Error('Failed to search issues');
    return response.json();
  },

  async getIssue(id: string): Promise<Issue> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/issues/${id}`);
    if (!response.ok) throw new Error('Failed to fetch issue');
    return response.json();
  },

  async getTrending(limit: number = 10): Promise<Issue[]> {
    const response = await fetchWithTimeout(`${API_BASE_URL}/issues/trending?limit=${limit}`);
    if (!response.ok) throw new Error('Failed to fetch trending issues');
    return response.json();
  },

  async sendFeedback(id: string, type: 'view' | 'useful'): Promise<void> {
    await fetchWithTimeout(`${API_BASE_URL}/issues/${id}/feedback?type=${type}`, {
      method: 'POST',
    });
  }
};
