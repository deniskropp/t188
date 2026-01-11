import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Wand2, History as HistoryIcon, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { loopApi } from '../lib/api';

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
  suggestions: string[];
}

export const Chat: React.FC<ChatProps> = ({ 
  onSendMessage, onClear, onSuggest, onPlan, messages, isProcessing, suggestions 
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
    
    // Log artistic action to the Loop Narrative Engine
    loopApi.logEntry(
      input.length > 50 ? 'reflection' : 'stroke', 
      input,
      { timestamp: Date.now() }
    ).catch(console.error);

    onSendMessage(input);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full glass rounded-3xl overflow-hidden border border-white/10">
      {/* Header */}
      <div className="p-4 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
        <div className="flex items-center gap-2">
          <HistoryIcon className="text-zinc-400 w-4 h-4" />
          <h2 className="text-sm font-semibold text-zinc-300">Narrative Thread</h2>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={onSuggest}
            className="p-2 hover:bg-white/5 rounded-lg text-zinc-400 hover:text-meta-accent transition-colors"
            title="Get Suggestions"
          >
            <Sparkles size={18} />
          </button>
          <button 
            onClick={onClear}
            className="p-2 hover:bg-red-500/10 rounded-lg text-zinc-400 hover:text-red-400 transition-colors"
            title="Reset Narrative"
          >
            <Trash2 size={18} />
          </button>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth">
        <AnimatePresence initial={false}>
          {messages.map((msg) => (
            <motion.div
              key={msg.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[85%] rounded-2xl p-4 ${
                msg.role === 'user' 
                  ? 'bg-meta-accent text-white shadow-[0_4px_15px_rgba(139,92,246,0.3)]' 
                  : 'bg-white/5 border border-white/10 text-zinc-200'
              }`}>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        {isProcessing && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
            <div className="bg-white/5 border border-white/10 rounded-2xl p-4 flex gap-1">
              <span className="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '0s' }}></span>
              <span className="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></span>
              <span className="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></span>
            </div>
          </motion.div>
        )}
      </div>

      {/* Suggestions Tray */}
      {suggestions.length > 0 && (
        <div className="px-4 py-3 flex gap-2 overflow-x-auto no-scrollbar border-t border-white/5 bg-black/20">
          {suggestions.map((s, idx) => (
            <button
              key={idx}
              onClick={() => setInput(s)}
              className="whitespace-nowrap px-3 py-1.5 rounded-full glass-accent text-xs text-meta-accent hover:bg-meta-accent/20 transition-all font-medium"
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 bg-white/[0.02]">
        <div className="relative flex items-center">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Guide the narrative..."
            className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-6 pr-24 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-meta-accent/50 focus:ring-1 focus:ring-meta-accent/50 transition-all shadow-inner"
          />
          <div className="absolute right-2 flex gap-1">
             <button
              type="button"
              onClick={() => { if(input.trim()) onPlan(input); }}
              className="p-2.5 text-meta-accent hover:bg-meta-accent/10 rounded-xl transition-colors"
              title="Pre-calculate Subconscious Plan"
            >
              <Wand2 size={20} />
            </button>
            <button
              type="submit"
              disabled={!input.trim() || isProcessing}
              className={`p-2.5 rounded-xl transition-all ${
                input.trim() && !isProcessing 
                  ? 'bg-meta-accent text-white shadow-lg shadow-meta-accent/20 hover:scale-105 active:scale-95' 
                  : 'bg-zinc-800 text-zinc-500'
              }`}
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};
