/**
 * MetaCognito API Client
 * Using native fetch to avoid external dependencies.
 */

export interface ApiResponse<T> {
  data: T;
  status: number;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || response.statusText);
  }

  return response.json();
}

export const lex = {
  chat: (message: string, mindState?: any) => 
    request<{ reply: string; graph_nodes: number }>('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message, mind_state: mindState }),
    }),
  
  getHistory: () => 
    request<any[]>('/api/history'),
};

export const sage = {
  getSuggestions: () => 
    request<{ suggestions: string[] }>('/api/suggestions'),
};

export const planner = {
  plan: (message: string) => 
    request<any>('/api/plan', {
      method: 'POST',
      body: JSON.stringify({ message }),
    }),
};

export const systemApi = {
  getStatus: () => 
    request<any>('/api/status'),
  
  getGraph: () => 
    request<{ nodes: any[]; edges: any[] }>('/api/graph'),
  
  reset: () => 
    request<{ status: string; message: string }>('/api/reset', {
      method: 'POST',
    }),
  
  transform: (instruction: string) => 
    request<any>('/api/transform', {
      method: 'POST',
      body: JSON.stringify({ instruction }),
    }),
};

export const loopApi = {
  getStatus: () => 
    request<any>('/api/loop/status'),
  
  logEntry: (actionType: string, content: string, metadata?: any, sentiment?: number) => 
    request<any>('/api/loop/entry', {
      method: 'POST',
      body: JSON.stringify({ action_type: actionType, content, metadata, sentiment }),
    }),
  
  claimBadge: (questId: string) => 
    request<any>(`/api/loop/quest/claim/${questId}`, {
      method: 'POST',
    }),
};
