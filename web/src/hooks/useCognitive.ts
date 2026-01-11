import { useState, useEffect } from 'react';

export type CognitivePhase = 'idle' | 'researcher' | 'analyst' | 'storyteller' | 'planner' | 'done';

export interface CognitiveState {
  phase: CognitivePhase;
  status: string;
  isOnline: boolean;
}

export function useCognitive() {
  const [state, setState] = useState<CognitiveState>({
    phase: 'idle',
    status: '',
    isOnline: false,
  });

  useEffect(() => {
    const eventSource = new EventSource('/api/events');

    eventSource.onopen = () => {
      setState(prev => ({ ...prev, isOnline: true }));
    };

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        let newPhase = state.phase;
        if (data.operation) {
          const op = data.operation.toLowerCase();
          if (op.includes('researcher')) newPhase = 'researcher';
          else if (op.includes('analyst')) newPhase = 'analyst';
          else if (op.includes('storyteller')) newPhase = 'storyteller';
          else if (op.includes('planner')) newPhase = 'planner';
          else if (op.includes('synthesis')) newPhase = 'storyteller';
        }

        setState(prev => ({
          ...prev,
          phase: newPhase,
          status: data.message || prev.status,
        }));
      } catch (err) {
        console.error('Cognitive Stream Parse Error:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('Cognitive Stream Error:', err);
      setState(prev => ({ ...prev, isOnline: false }));
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const setPhase = (phase: CognitivePhase) => setState(prev => ({ ...prev, phase }));
  const setStatus = (status: string) => setState(prev => ({ ...prev, status }));

  return { ...state, setPhase, setStatus };
}
