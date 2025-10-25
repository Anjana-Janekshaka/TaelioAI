import { useState, useCallback } from 'react';
import { apiService } from '@/lib/api';

export interface ApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useApi<T>() {
  const [state, setState] = useState<ApiState<T>>({
    data: null,
    loading: false,
    error: null,
  });

  const execute = useCallback(async (apiCall: () => Promise<T>) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const data = await apiCall();
      setState({ data, loading: false, error: null });
      return data;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
      setState(prev => ({ ...prev, loading: false, error: errorMessage }));
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  return {
    ...state,
    execute,
    reset,
  };
}

export function useIdeaGeneration() {
  const { data, loading, error, execute, reset } = useApi();

  const generateIdea = useCallback(async (prompt: string, genre: string, tone?: string) => {
    return execute(() => apiService.generateIdea({ prompt, genre, tone }));
  }, [execute]);

  return {
    idea: data,
    loading,
    error,
    generateIdea,
    reset,
  };
}

export function useStoryWriting() {
  const { data, loading, error, execute, reset } = useApi();

  const writeStory = useCallback(async (request: {
    title: string;
    genre: string;
    tone?: string;
    outline?: string;
    characters?: string;
    setting?: string;
  }) => {
    return execute(() => apiService.writeStory(request));
  }, [execute]);

  return {
    story: data,
    loading,
    error,
    writeStory,
    reset,
  };
}

export function useStreamingStoryWriting() {
  const [story, setStory] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [metadata, setMetadata] = useState<any>(null);

  const writeStoryStreaming = useCallback(async (request: {
    title: string;
    genre: string;
    tone?: string;
    outline?: string;
    characters?: string;
    setting?: string;
  }, streamingSpeed: string = "normal") => {
    setLoading(true);
    setError(null);
    setStory('');
    setMetadata(null);

    try {
      await apiService.writeStoryStreaming(request, (chunk) => {
        if (chunk.type === 'content') {
          setStory(prev => prev + chunk.content);
        } else if (chunk.type === 'metadata') {
          setMetadata(chunk);
        } else if (chunk.type === 'error') {
          setError(chunk.error);
        } else if (chunk.type === 'complete') {
          setLoading(false);
        }
      }, streamingSpeed);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setStory('');
    setLoading(false);
    setError(null);
    setMetadata(null);
  }, []);

  return {
    story,
    loading,
    error,
    metadata,
    writeStoryStreaming,
    reset,
  };
}

export function useFullWorkflow() {
  const { data, loading, error, execute, reset } = useApi();

  const generateFullStory = useCallback(async (prompt: string, genre?: string, tone?: string) => {
    return execute(() => apiService.generateFullStory({ prompt, genre, tone }));
  }, [execute]);

  return {
    result: data,
    loading,
    error,
    generateFullStory,
    reset,
  };
}
