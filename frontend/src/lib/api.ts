import axios from 'axios';

export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ---- Types (mirror backend Pydantic schemas) ----

export interface IdeaRequest {
  prompt: string;
  genre?: string;
  tone?: string;
}

export interface IdeaResponse {
  title: string;
  genre: string;
  tone: string;
  outline: string;
  characters?: string[] | null;
  setting?: string | null;
}

export interface StoryRequest {
  title: string;
  genre: string;
  outline: string;
  tone?: string;
  characters?: string;
  setting?: string;
}

export interface StoryResponse {
  story: string;
}

export interface FullStoryRequest {
  prompt: string;
  genre?: string;
  tone?: string;
}

export interface FullStoryResponse {
  idea: IdeaResponse;
  story: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user_id: string;
  email: string;
  role: string;
}

export interface StoryEditRequest {
  story: string;
  edit_instructions: string;
  title?: string;
  genre?: string;
}

export interface StoryEditResponse {
  success: boolean;
  edited_story: string;
  original_story: string;
  edit_instructions: string;
  title: string;
  genre: string;
  metadata: Record<string, any>;
}

export interface ModerationMetrics {
  total_content_moderated: number;
  total_violations_found: number;
  total_unsafe_content: number;
  average_safety_score: number;
  violations_by_type: Record<string, number>;
  content_by_type: Record<string, number>;
  safety_score_distribution: Record<string, number>;
  period_days: number;
}

export interface ModerationViolation {
  violation_type: string;
  count: number;
  severity: string;
  percentage: number;
}

export interface ModerationStats {
  user_id: string;
  period_days: number;
  total_moderations: number;
  violations_found: number;
  unsafe_content_count: number;
  average_safety_score: number;
  violation_breakdown: ModerationViolation[];
  content_type_breakdown: Record<string, number>;
  safety_score_ranges: Record<string, number>;
}

export type StreamChunk =
  | { type: 'content'; content: string; is_final?: boolean }
  | {
      type: 'metadata';
      provider: string;
      model: string;
      tokens_in?: number;
      tokens_out?: number;
      cost_usd?: number;
    }
  | { type: 'error'; error: string }
  | { type: 'complete' };

// ---- HTTP client ----

function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  try {
    return localStorage.getItem('auth_token');
  } catch {
    return null;
  }
}

function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

const client = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

client.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ---- API service ----

export const apiService = {
  async login(email: string): Promise<LoginResponse> {
    const { data } = await client.post<LoginResponse>('/auth/login', { email });
    return data;
  },

  async generateIdea(request: IdeaRequest): Promise<IdeaResponse> {
    const { data } = await client.post<IdeaResponse>('/idea/generate-idea', request);
    return data;
  },

  async writeStory(request: StoryRequest): Promise<StoryResponse> {
    const { data } = await client.post<StoryResponse>('/story/write-story', request);
    return data;
  },

  // Backend streams "data: {json}\n\n" events; each parsed event is passed to onChunk.
  async writeStoryStreaming(
    request: StoryRequest,
    onChunk: (chunk: StreamChunk) => void,
    streamingSpeed: string = 'normal'
  ): Promise<void> {
    const url = `${API_URL}/story/write-story-stream?streaming_speed=${encodeURIComponent(streamingSpeed)}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify(request),
    });

    if (!response.ok || !response.body) {
      let detail = `Request failed with status ${response.status}`;
      try {
        const body = await response.json();
        if (body?.detail) detail = body.detail;
      } catch {
        // response wasn't JSON
      }
      throw new Error(detail);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    const handleEvent = (event: string) => {
      const line = event.split('\n').find((l) => l.startsWith('data:'));
      if (!line) return;
      try {
        onChunk(JSON.parse(line.slice(5).trim()) as StreamChunk);
      } catch {
        // ignore malformed event
      }
    };

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop() ?? '';
      events.forEach(handleEvent);
    }
    if (buffer.trim()) handleEvent(buffer);
  },

  async generateFullStory(request: FullStoryRequest): Promise<FullStoryResponse> {
    const { data } = await client.post<FullStoryResponse>('/workflow/generate-full-story', request);
    return data;
  },

  async editStory(request: StoryEditRequest): Promise<StoryEditResponse> {
    const { data } = await client.post<StoryEditResponse>('/story-editor/edit', request);
    return data;
  },

  async getModerationMetrics(days: number = 30): Promise<ModerationMetrics> {
    const { data } = await client.get<ModerationMetrics>('/moderation/metrics', { params: { days } });
    return data;
  },

  async getModerationStats(days: number = 30): Promise<ModerationStats> {
    const { data } = await client.get<ModerationStats>('/moderation/stats', { params: { days } });
    return data;
  },
};

export default apiService;
