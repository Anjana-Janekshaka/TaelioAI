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
