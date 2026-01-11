import React from 'react';
import { Eye, Search, Brain, Sparkles, ClipboardList } from 'lucide-react';
import { motion } from 'framer-motion';

interface SubconsciousMonitorProps {
  phase: 'idle' | 'researcher' | 'analyst' | 'storyteller' | 'planner' | 'done';
  status?: string;
}

const phases = [
  { id: 'researcher', icon: Search, label: 'Researcher', desc: 'Finding hidden cues' },
  { id: 'analyst', icon: Eye, label: 'Analyst', desc: 'Clustering patterns' },
  { id: 'storyteller', icon: Sparkles, label: 'Subconscious Storyteller', desc: 'Synthesizing vibes' },
  { id: 'planner', icon: ClipboardList, label: 'Subconscious Planner', desc: 'Sequencing implicit plan' },
];

export const SubconsciousMonitor: React.FC<SubconsciousMonitorProps> = ({ phase, status }) => {
  return (
    <div className="glass p-6 rounded-2xl w-full max-w-md">
      <div className="flex items-center gap-3 mb-6">
        <Brain className="text-meta-accent w-6 h-6 animate-pulse" />
        <h2 className="text-xl font-bold font-display tracking-tight text-white">Subconscious Monitor</h2>
      </div>

      <div className="space-y-4">
        {phases.map((p, idx) => {
          const isActive = phase === p.id;
          const isDone = phases.findIndex(ph => ph.id === phase) > idx || phase === 'done';
          const Icon = p.icon;

          return (
            <motion.div 
              key={p.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className={`relative flex items-center gap-4 p-3 rounded-xl transition-all duration-500 ${
                isActive ? 'bg-meta-accent/20 border border-meta-accent/50 shadow-[0_0_20px_rgba(139,92,246,0.2)]' : 
                isDone ? 'opacity-50' : 'opacity-30'
              }`}
            >
              <div className={`p-2 rounded-lg ${isActive ? 'bg-meta-accent text-white' : 'bg-zinc-800 text-zinc-400'}`}>
                <Icon size={18} />
              </div>
              <div className="flex-1">
                <div className="text-sm font-semibold text-white">{p.label}</div>
                <div className="text-xs text-zinc-400">{p.desc}</div>
              </div>
              {isActive && (
                <div className="flex gap-1">
                  <span className="w-1.5 h-1.5 bg-meta-accent rounded-full animate-bounce" style={{ animationDelay: '0s' }}></span>
                  <span className="w-1.5 h-1.5 bg-meta-accent rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
                  <span className="w-1.5 h-1.5 bg-meta-accent rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
      
      {phase !== 'idle' && status && (
        <div className="mt-6 p-3 rounded-xl bg-white/[0.03] border border-white/5">
           <div className="text-[10px] uppercase font-bold tracking-widest text-zinc-500 mb-1">Live Trace</div>
           <div className="text-xs text-meta-accent font-medium italic animate-pulse">
              {status}
           </div>
        </div>
      )}
      
      {phase === 'idle' && (
        <div className="mt-6 text-center text-xs text-zinc-500 italic">
          Waiting for neural activity...
        </div>
      )}
    </div>
  );
};
