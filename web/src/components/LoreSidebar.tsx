import React from 'react';
import { User, MapPin, Book, Box, Layers, Search, Sparkles, ClipboardList } from 'lucide-react';
import { motion } from 'framer-motion';

interface Entity {
  id: string;
  label: string;
  type: string;
  properties: any;
}

interface LoreSidebarProps {
  entities: Entity[];
  selectedNodeId?: string | null;
  onNodeClick?: (nodeId: string) => void;
}

const typeIcons: Record<string, any> = {
  'Character': User,
  'Location': MapPin,
  'Item': Box,
  'Event': Book,
  'Concept': Layers,
  'LatentPattern': Search,
  'DreamNarrative': Sparkles,
  'ImplicitPlan': ClipboardList,
};

const sectionOrder = [
  'LatentPattern',
  'DreamNarrative',
  'ImplicitPlan',
  'Concept',
  'Character',
  'Location',
  'Event',
];

const labelOverrides: Record<string, string> = {
  'LatentPattern': 'LATENTPATTERNS',
  'DreamNarrative': 'DREAM/NARRATIVES',
  'ImplicitPlan': 'IMPLICITPLANS',
  'Concept': 'CONCEPTS',
  'Character': 'CHARACTERS',
  'Location': 'LOCATIONS',
  'Event': 'EVENTS',
};

export const LoreSidebar: React.FC<LoreSidebarProps> = ({ entities, selectedNodeId, onNodeClick }) => {
  const selectedEntity = entities.find(e => e.id === selectedNodeId);

  const grouped = entities.reduce((acc, entity) => {
    const type = entity.type;
    if (!acc[type]) acc[type] = [];
    acc[type].push(entity);
    return acc;
  }, {} as Record<string, Entity[]>);

  const sortedTypes = Object.keys(grouped).sort((a, b) => {
    const idxA = sectionOrder.indexOf(a);
    const idxB = sectionOrder.indexOf(b);
    if (idxA === -1 && idxB === -1) return a.localeCompare(b);
    if (idxA === -1) return 1;
    if (idxB === -1) return -1;
    return idxA - idxB;
  });

  return (
    <div className="bg-[#0a0a0c] h-full rounded-[2.5rem] overflow-hidden flex flex-col border border-white/5 shadow-2xl">
      <div className="p-8 border-b border-white/5 bg-[#0f1117]">
        <h2 className="text-xl font-bold text-white tracking-tight leading-none mb-1">Lore Library</h2>
        <p className="text-[10px] text-zinc-600 font-bold uppercase tracking-[0.1em]">Foundational knowledge of the world</p>
      </div>

      <div className="flex-1 overflow-y-auto p-2 py-6 space-y-6 no-scrollbar">
        {selectedEntity && (
           <motion.div 
             initial={{ opacity: 0, scale: 0.95 }}
             animate={{ opacity: 1, scale: 1 }}
             className="mx-4 p-5 rounded-[2rem] bg-meta-accent/10 border border-meta-accent/30 shadow-lg shadow-meta-accent/5 mb-8"
           >
              <div className="flex items-center justify-between mb-4">
                 <span className="text-[10px] font-black uppercase tracking-[0.2em] text-meta-accent">Entity Detail</span>
                 <button onClick={() => onNodeClick?.('')} className="text-zinc-600 hover:text-white text-[9px] uppercase font-black tracking-widest transition-colors">Close</button>
              </div>
              <h3 className="text-xl font-black italic tracking-tighter text-white mb-4">{selectedEntity.label}</h3>
              <div className="space-y-4">
                 {selectedEntity.properties && Object.entries(selectedEntity.properties).map(([k, v]) => (
                    <div key={k} className="bg-white/5 p-3 rounded-2xl border border-white/5">
                       <div className="text-[8px] uppercase font-black tracking-[0.2em] text-zinc-600 mb-1">{k}</div>
                       <div className="text-xs text-zinc-300 font-medium leading-relaxed">{String(v)}</div>
                    </div>
                 ))}
              </div>
           </motion.div>
        )}

        {sortedTypes.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20 opacity-10">
            <Book size={64} strokeWidth={1} />
            <p className="text-[10px] uppercase font-black tracking-widest mt-4">Library Empty</p>
          </div>
        ) : (
          sortedTypes.map((type, gIdx) => {
            const Icon = typeIcons[type] || Layers;
            const items = grouped[type];
            return (
              <motion.div 
                key={type}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: gIdx * 0.05 }}
                className="space-y-1"
              >
                <div className="flex items-center gap-2 mb-2 px-4 group">
                  <Icon size={12} className="text-meta-accent/60 group-hover:text-meta-accent transition-colors" />
                  <h3 className="text-[9px] font-black uppercase tracking-[0.2em] text-zinc-600 group-hover:text-zinc-400 transition-colors">
                    {labelOverrides[type] || type.toUpperCase()}
                  </h3>
                </div>
                <div className="px-2 space-y-1">
                  {items.map((item) => {
                    const isSelected = item.id === selectedNodeId;
                    return (
                      <motion.div 
                        key={item.id}
                        whileHover={{ x: 4 }}
                        onClick={() => onNodeClick?.(item.id)}
                        className={`group p-4 rounded-2xl cursor-pointer transition-all border ${
                          isSelected 
                            ? 'bg-meta-accent text-white shadow-xl shadow-meta-accent/20 border-meta-accent/50' 
                            : 'bg-white/[0.02] hover:bg-white/[0.05] border-transparent hover:border-white/5'
                        }`}
                      >
                        <div className={`text-[11px] font-bold transition-colors ${isSelected ? 'text-white' : 'text-zinc-400 group-hover:text-zinc-200'}`}>
                          {item.label}
                        </div>
                      </motion.div>
                    );
                  })}
                </div>
              </motion.div>
            );
          })
        )}
      </div>
      
      <div className="p-6 bg-[#0f1117] border-t border-white/5">
         <div className="flex justify-between items-center text-[9px] font-black uppercase tracking-[0.3em] text-zinc-700">
            <span className="flex items-center gap-2">
               <div className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse" />
               Graph Health
            </span>
            <span className="text-meta-accent/50">Optimal</span>
         </div>
      </div>
    </div>
  );
};
