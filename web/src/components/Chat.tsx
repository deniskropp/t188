import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Wand2, History as HistoryIcon, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
}

interface ChatProps {
  onSendMessage: (message: string) => void;
  onClear: () => void;
  onSuggest: () => void;
  onPlan: (message: string) => void;
  messages: Message[];
  isProcessing: boolean;
}

export const Chat: React.FC<ChatProps> = ({ 
  onSendMessage, onClear, onSuggest, onPlan, messages, isProcessing 
}) => {
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || isProcessing) return;
    
    onSendMessage(input);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-[#161922] border border-white/5 shadow-2xl rounded-[3rem] overflow-hidden">
      {/* Header */}
      <div className="px-8 py-5 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
        <div className="flex items-center gap-3">
          <HistoryIcon className="text-zinc-600 w-4 h-4" />
          <h2 className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-500 italic">Narrative Thread</h2>
        </div>
        <div className="flex gap-1">
          <button 
            onClick={onSuggest}
            className="p-2.5 hover:bg-white/5 rounded-2xl text-zinc-600 hover:text-meta-accent transition-all"
            title="Get Suggestions"
          >
            <Sparkles size={18} />
          </button>
          <button 
            onClick={onClear}
            className="p-2.5 hover:bg-red-500/10 rounded-2xl text-zinc-600 hover:text-red-400 transition-all"
            title="Reset Narrative"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-8 space-y-6 scroll-smooth">
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 15, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[75%] rounded-[2rem] p-6 shadow-xl ${
                msg.role === 'user' 
                  ? 'bg-gradient-to-br from-meta-accent to-purple-800 text-white border border-white/10' 
                  : 'bg-white/[0.02] border border-white/5 text-zinc-300'
              }`}>
                <p className="text-[13px] font-medium leading-[1.6] tracking-tight">{msg.content}</p>
                {msg.role === 'assistant' && (
                  <div className="flex gap-1 mt-4">
                     <div className="w-6 h-1 bg-meta-accent/30 rounded-full" />
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {isProcessing && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
            <div className="bg-white/5 border border-white/5 rounded-[1.5rem] p-4 flex gap-1.5 items-center">
              {[0, 1, 2].map(i => (
                <motion.div 
                  key={i}
                  animate={{ scale: [1, 1.5, 1], opacity: [0.3, 1, 0.3] }}
                  transition={{ repeat: Infinity, duration: 1, delay: i * 0.2 }}
                  className="w-1 h-1 bg-meta-accent rounded-full" 
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>

      {/* Input Form */}
      <div className="p-6 bg-white/[0.01] border-t border-white/5">
         <form onSubmit={handleSubmit} className="relative group">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Guide the narrative..."
              className="w-full bg-white/[0.03] border border-white/10 rounded-[2rem] py-5 px-8 pr-32 text-xs font-bold text-white placeholder:text-zinc-600 focus:outline-none focus:border-meta-accent/40 focus:bg-white/[0.04] transition-all"
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex gap-2">
               <button
                type="button"
                onClick={() => { if(input.trim()) onPlan(input); }}
                className="p-3 text-meta-accent/60 hover:text-meta-accent hover:bg-meta-accent/10 rounded-2xl transition-all"
              >
                <Wand2 size={20} />
              </button>
              <button
                type="submit"
                disabled={!input.trim() || isProcessing}
                className={`p-3 rounded-2xl transition-all ${
                  input.trim() && !isProcessing 
                    ? 'bg-meta-accent text-white shadow-lg shadow-meta-accent/20 hover:scale-105 active:scale-95' 
                    : 'bg-zinc-800 text-zinc-500'
                }`}
              >
                <Send size={20} />
              </button>
            </div>
         </form>
      </div>
    </div>
  );
};
