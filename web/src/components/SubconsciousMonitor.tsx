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
    <div className="w-full">
      <div className="flex items-center gap-3 mb-5 px-1">
        <div className="p-1.5 bg-meta-accent/10 rounded-lg">
           <Brain size={16} className="text-meta-accent" />
        </div>
        <h2 className="text-[10px] font-black uppercase tracking-[0.2em] text-zinc-500 italic">Subconscious Monitor</h2>
      </div>

      <div className="space-y-2">
        {phases.map((p, idx) => {
          const isActive = phase === p.id;
          const isDone = phases.findIndex(ph => ph.id === phase) > idx || phase === 'done';
          const Icon = p.icon;

          return (
            <motion.div 
              key={p.id}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.05 }}
              className={`relative flex items-center gap-4 p-3 rounded-2xl transition-all duration-500 border ${
                isActive ? 'bg-meta-accent/10 border-meta-accent/30 shadow-lg shadow-meta-accent/5' : 
                'bg-white/[0.02] border-white/5 opacity-50'
              } ${!isActive && !isDone ? 'opacity-20 grayscale' : ''}`}
            >
              <div className={`p-2 rounded-xl ${isActive ? 'bg-meta-accent text-white shadow-lg shadow-meta-accent/40' : 'bg-zinc-800/50 text-zinc-500'}`}>
                <Icon size={16} />
              </div>
              <div className="flex-1 min-w-0">
                <div className={`text-[11px] font-bold ${isActive ? 'text-white' : 'text-zinc-500'}`}>{p.label}</div>
                <div className="text-[9px] text-zinc-600 font-medium truncate">{p.desc}</div>
              </div>
              
              {isActive && (
                <div className="flex gap-1 pr-2">
                   <motion.div 
                    animate={{ scale: [1, 1.5, 1], opacity: [0.5, 1, 0.5] }}
                    transition={{ repeat: Infinity, duration: 2 }}
                    className="w-1 h-1 bg-meta-accent rounded-full" 
                   />
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
      
      {phase !== 'idle' && status && (
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 rounded-3xl bg-meta-accent/5 border border-meta-accent/10 relative overflow-hidden"
        >
           <div className="absolute top-0 left-0 w-1 h-full bg-meta-accent/30" />
           <div className="text-[8px] font-black uppercase tracking-[0.2em] text-meta-accent/60 mb-1.5">Neural Trace</div>
           <div className="text-[10px] text-zinc-300 font-bold italic leading-relaxed">
              {status}
           </div>
        </motion.div>
      )}
    </div>
  );
};
