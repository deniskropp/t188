import { useState, useEffect, useCallback } from 'react';
import { SubconsciousMonitor } from './components/SubconsciousMonitor';
import { GraphViewer } from './components/GraphViewer';
import { Chat } from './components/Chat';
import { LoreSidebar } from './components/LoreSidebar';
import { LoopDashboard } from './components/LoopDashboard';
import { motion, AnimatePresence } from 'framer-motion';
import { BrainCircuit, Info, Layers } from 'lucide-react';
import { useCognitive } from './hooks/useCognitive';
import { lex, sage, planner, systemApi } from './lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const { phase, status, setPhase, setStatus } = useCognitive();
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [stagedPlan, setStagedPlan] = useState<any>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const [graphRes, historyRes] = await Promise.all([
        systemApi.getGraph(),
        lex.getHistory()
      ]);
      setNodes(graphRes.nodes);
      setEdges(graphRes.edges);
      
      const historyMessages: Message[] = historyRes.flatMap((h: any, idx: number) => [
        { id: `u-${idx}`, role: 'user', content: h.user },
        { id: `a-${idx}`, role: 'assistant', content: h.story }
      ]);
      setMessages(historyMessages);
    } catch (err) {
      console.error('Failed to fetch data:', err);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleSendMessage = async (content: string) => {
    setIsProcessing(true);
    setStatus('Initiating narrative request...');
    
    // Add user message to UI immediately
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content };
    setMessages(prev => [...prev, userMsg]);

    try {
      const res = await lex.chat(content, stagedPlan);
      
      const assistantMsg: Message = { 
        id: (Date.now() + 1).toString(), 
        role: 'assistant', 
        content: res.reply 
      };
      setMessages(prev => [...prev, assistantMsg]);
      setStagedPlan(null);
      setPhase('done');
      fetchData();
    } catch (err) {
      console.error('Chat error:', err);
    } finally {
      setIsProcessing(false);
      setTimeout(() => setPhase('idle'), 2000);
    }
  };

  const handlePlan = async (content: string) => {
    setIsProcessing(true);
    setPhase('researcher');
    try {
      // Simulate phase transitions for UI charm - but keep real plan call
      setTimeout(() => setPhase('analyst'), 1000);
      setTimeout(() => setPhase('storyteller'), 2500);
      setTimeout(() => setPhase('planner'), 4000);

      const res = await planner.plan(content);
      setStagedPlan(res);
      
      // Add a system feedback message
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'system',
        content: `Subconscious plan staged for: "${content}"`
      }]);
      
      setPhase('done');
      fetchData();
    } catch (err) {
      console.error('Plan error:', err);
    } finally {
      setIsProcessing(false);
      setTimeout(() => setPhase('idle'), 2000);
    }
  };

  const handleSuggest = async () => {
    try {
      const res = await sage.getSuggestions();
      setSuggestions(res.suggestions);
    } catch (err) {
      console.error('Suggestions error:', err);
    }
  };

  const handleClear = async () => {
    if (window.confirm('Wipe all narrative history and world state?')) {
      await systemApi.reset();
      setMessages([]);
      setNodes([]);
      setEdges([]);
      setStagedPlan(null);
      setSuggestions([]);
      fetchData();
    }
  };

  return (
    <div className="flex h-screen w-full bg-[#0a0c10] text-white overflow-hidden font-sans selection:bg-meta-accent/30">
      {/* 1. Left Navigation Sidebar */}
      <aside className="w-[320px] shrink-0 border-r border-white/5 bg-[#0f1117] flex flex-col p-4 gap-6 relative z-30">
        <header className="flex items-center gap-3 mb-4">
           <div className="p-2.5 bg-meta-accent/10 rounded-2xl border border-meta-accent/20 shadow-lg shadow-meta-accent/5">
              <BrainCircuit className="text-meta-accent w-6 h-6" />
           </div>
           <div>
              <h1 className="text-xl font-black tracking-tighter uppercase italic bg-gradient-to-br from-white to-zinc-500 bg-clip-text text-transparent">MetaCognito</h1>
              <div className="text-[9px] text-zinc-600 font-bold tracking-[0.2em] uppercase">Orchestration Engine</div>
           </div>
        </header>

        {/* Global Navigation */}
        <nav className="flex flex-col gap-1">
          <button className="flex items-center gap-3 p-3 rounded-xl bg-meta-accent/10 text-meta-accent border border-meta-accent/10 font-bold text-xs uppercase tracking-widest transition-all">
             <BrainCircuit size={18} />
             Story Engine
          </button>
          <button className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 text-zinc-500 hover:text-zinc-300 font-bold text-xs uppercase tracking-widest transition-all">
             <Layers size={18} />
             Transformations
          </button>
        </nav>

        {/* Status Monitoring */}
        <SubconsciousMonitor phase={phase} status={status} />

        {/* The Dopamin Engine Dashboard Integration */}
        <div className="flex-1 min-h-0 overflow-y-auto no-scrollbar py-2">
           <LoopDashboard />
        </div>

        {/* System Summary */}
        <div className="bg-[#161922] p-6 rounded-[2rem] border border-white/5 mt-auto">
            <div className="flex items-center justify-between mb-5">
               <span className="text-[10px] font-black uppercase tracking-[0.3em] text-zinc-600 italic">System Status</span>
               <div className="flex items-center gap-2 px-3 py-1 bg-green-500/5 rounded-full border border-green-500/20">
                  <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-[8px] font-black text-green-500 uppercase tracking-widest">Online</span>
               </div>
            </div>
            
            <div className="grid grid-cols-2 gap-3 mb-6">
               <div className="bg-white/[0.03] p-4 rounded-2xl border border-white/5">
                  <div className="text-[8px] font-black text-zinc-600 uppercase tracking-widest mb-1.5">Entities</div>
                  <div className="text-2xl font-black italic tracking-tighter">{nodes.length}</div>
               </div>
               <div className="bg-white/[0.03] p-4 rounded-2xl border border-white/5">
                  <div className="text-[8px] font-black text-zinc-600 uppercase tracking-widest mb-1.5">Relations</div>
                  <div className="text-2xl font-black italic tracking-tighter">{edges.length}</div>
               </div>
            </div>

            <button 
              onClick={handleClear}
              className="w-full flex items-center justify-center gap-2 py-4 rounded-[1.5rem] border border-red-500/10 text-red-500/40 hover:text-red-400 hover:bg-red-500/5 transition-all text-[9px] font-black uppercase tracking-[0.2em]"
            >
               <Info size={14} className="opacity-50" />
               Clear World State
            </button>
        </div>
      </aside>

      {/* 2. Main Content Area: Immersive Graph + Chat */}
      <main className="flex-1 relative flex flex-col bg-[#0d0f14]">
        {/* Immersive Graph Viewer */}
        <div className="absolute inset-0 z-0">
           <GraphViewer 
             nodes={nodes} 
             edges={edges} 
             selectedNodeId={selectedNodeId} 
             onNodeClick={setSelectedNodeId} 
           />
        </div>

        {/* Floating Top Bar (Controls for Graph) */}
        <div className="absolute top-6 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2 p-1 bg-black/40 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl">
           <button className="px-4 py-2 hover:bg-white/5 rounded-xl text-[10px] font-black uppercase tracking-widest text-zinc-400 hover:text-white transition-all">Search Entities</button>
           <div className="w-px h-4 bg-white/10 mx-1" />
           <button className="px-4 py-2 hover:bg-white/5 rounded-xl text-[10px] font-black uppercase tracking-widest text-zinc-400 hover:text-white transition-all">Recent Pins</button>
        </div>

        {/* Floating Right Sidebar: Lore Info Box (Optional Overlay) */}
        <AnimatePresence>
          {selectedNodeId && (
            <motion.div 
              initial={{ x: 400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 400, opacity: 0 }}
              className="absolute right-6 top-6 bottom-6 w-[350px] z-20"
            >
               <LoreSidebar 
                 entities={nodes} 
                 selectedNodeId={selectedNodeId} 
                 onNodeClick={setSelectedNodeId} 
               />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Central Bottom Chat Overlay (Matches Screenshot) */}
        <div className="absolute bottom-6 left-6 right-6 z-20 pointer-events-none flex flex-col justify-end">
           <div className="max-w-5xl mx-auto w-full flex flex-col gap-4 max-h-[85vh]">
              {/* Context-aware suggestion chips */}
              {suggestions.length > 0 && (
                <motion.div 
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  className="flex justify-center gap-2 mb-2 pointer-events-auto"
                >
                   {suggestions.map((s, i) => (
                     <button 
                       key={i} 
                       onClick={() => handleSendMessage(s)}
                       className="px-4 py-2 bg-black/60 backdrop-blur-2xl border border-white/10 rounded-full text-[10px] font-black text-meta-accent hover:border-meta-accent/50 hover:bg-meta-accent/10 transition-all shadow-2xl uppercase tracking-tighter"
                     >
                       {s}
                     </button>
                   ))}
                </motion.div>
              )}

              <div className="pointer-events-auto min-h-0 flex flex-col">
                <Chat 
                  onSendMessage={handleSendMessage}
                  onClear={handleClear}
                  onSuggest={handleSuggest}
                  onPlan={handlePlan}
                  messages={messages.filter(m => m.role !== 'system')}
                  isProcessing={isProcessing}
                />
              </div>
              
              <div className="flex justify-center pointer-events-auto">
                 <div className="text-[9px] text-zinc-600 font-bold uppercase tracking-[0.3em] bg-black/40 px-4 py-1.5 rounded-full border border-white/5 backdrop-blur-md">
                    Orchestration Engine Ready
                 </div>
              </div>
           </div>
        </div>
      </main>
    </div>
  );
}

export default App;
