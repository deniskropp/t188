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
    <div className="flex flex-col h-full bg-meta-surface border border-meta-border shadow-2xl rounded-2xl overflow-hidden transition-colors duration-300">
      {/* Header */}
      <div className="px-6 py-4 border-b border-meta-border flex items-center justify-between bg-meta-surface/50">
        <div className="flex items-center gap-3">
          <HistoryIcon className="text-meta-muted w-4 h-4" />
          <h2 className="text-[10px] font-black uppercase tracking-[0.3em] text-meta-muted italic">Narrative Thread</h2>
        </div>
        <div className="flex gap-1">
          <button 
            onClick={onSuggest}
            className="p-2.5 hover:bg-meta-surface-hover rounded-lg text-meta-muted hover:text-meta-accent transition-all"
            title="Get Suggestions"
          >
            <Sparkles size={18} />
          </button>
          <button 
            onClick={onClear}
            className="p-2.5 hover:bg-red-500/10 rounded-lg text-meta-muted hover:text-red-500 transition-all"
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
              <div className={`max-w-[75%] rounded-xl p-4 shadow-xl ${
                msg.role === 'user' 
                  ? 'bg-gradient-to-br from-meta-accent to-purple-800 text-white border border-white/10' 
                  : 'bg-meta-surface-hover border border-meta-border text-meta-main'
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
            <div className="bg-meta-surface-hover border border-meta-border rounded-[1.5rem] p-4 flex gap-1.5 items-center">
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
      <div className="p-6 bg-meta-surface/50 border-t border-meta-border">
         <form onSubmit={handleSubmit} className="relative group">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Guide the narrative..."
              className="w-full bg-meta-surface-hover border border-meta-border rounded-xl py-4 px-6 pr-32 text-xs font-bold text-meta-main placeholder:text-meta-muted focus:outline-none focus:border-meta-accent/40 focus:bg-meta-surface transition-all"
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2 flex gap-2">
               <button
                type="button"
                onClick={() => { if(input.trim()) onPlan(input); }}
                className="p-3 text-meta-accent/60 hover:text-meta-accent hover:bg-meta-accent/10 rounded-lg transition-all"
              >
                <Wand2 size={20} />
              </button>
              <button
                type="submit"
                disabled={!input.trim() || isProcessing}
                className={`p-3 rounded-lg transition-all ${
                  input.trim() && !isProcessing 
                    ? 'bg-meta-accent text-white shadow-lg shadow-meta-accent/20 hover:scale-105 active:scale-95' 
                    : 'bg-meta-surface-hover text-meta-muted'
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
