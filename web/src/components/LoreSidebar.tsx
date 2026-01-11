import React from 'react';
import { User, MapPin, Book, Box, Layers } from 'lucide-react';
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
};

export const LoreSidebar: React.FC<LoreSidebarProps> = ({ entities, selectedNodeId, onNodeClick }) => {
  const selectedEntity = entities.find(e => e.id === selectedNodeId);

  const grouped = entities.reduce((acc, entity) => {
    if (entity.type.includes('Subconscious')) return acc; // Hide subconscious nodes
    if (!acc[entity.type]) acc[entity.type] = [];
    acc[entity.type].push(entity);
    return acc;
  }, {} as Record<string, Entity[]>);

  return (
    <div className="glass h-full rounded-3xl overflow-hidden flex flex-col border border-white/10">
      <div className="p-6 border-b border-white/5 bg-white/[0.02]">
        <h2 className="text-xl font-bold text-white tracking-tight">Lore Library</h2>
        <p className="text-xs text-zinc-500 mt-1">Foundational knowledge of the world</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-8 scroll-smooth">
        {selectedEntity && (
           <motion.div 
             initial={{ opacity: 0, height: 0 }}
             animate={{ opacity: 1, height: 'auto' }}
             className="p-4 rounded-2xl bg-meta-accent/10 border border-meta-accent/30 shadow-[0_0_20px_rgba(139,92,246,0.1)] mb-4"
           >
              <div className="flex items-center justify-between mb-2">
                 <span className="text-[10px] font-bold uppercase tracking-widest text-meta-accent">Entity Detail</span>
                 <button onClick={() => onNodeClick?.('')} className="text-zinc-500 hover:text-white text-[10px] uppercase font-bold">Close</button>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">{selectedEntity.label}</h3>
              <div className="space-y-4">
                 {selectedEntity.properties && Object.entries(selectedEntity.properties).map(([k, v]) => (
                    <div key={k}>
                       <div className="text-[9px] uppercase font-bold tracking-tighter text-zinc-500">{k}</div>
                       <div className="text-xs text-zinc-300 leading-relaxed">{String(v)}</div>
                    </div>
                 ))}
              </div>
           </motion.div>
        )}

        {Object.entries(grouped).length === 0 ? (
          <div className="flex flex-col items-center justify-center h-40 opacity-20">
            <Book size={48} className="mb-2" />
            <p className="text-xs italic">No lore discovered yet...</p>
          </div>
        ) : (
          Object.entries(grouped).map(([type, items], gIdx) => {
            const Icon = typeIcons[type] || Layers;
            return (
              <motion.div 
                key={type}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: gIdx * 0.1 }}
              >
                <div className="flex items-center gap-2 mb-3 px-2">
                  <Icon size={14} className="text-meta-accent" />
                  <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500">{type}s</h3>
                  <span className="flex-1 border-b border-white/[0.05] ml-1"></span>
                </div>
                  {items.map((item) => {
                    const isSelected = item.id === selectedNodeId;
                    return (
                      <div 
                        key={item.id}
                        onClick={() => onNodeClick?.(item.id)}
                        className={`group p-3 rounded-xl cursor-pointer transition-all ${
                          isSelected 
                            ? 'bg-meta-accent text-white shadow-[0_4px_15px_rgba(139,92,246,0.3)] ring-1 ring-white/20' 
                            : 'bg-white/[0.03] hover:bg-white/[0.07] border border-transparent hover:border-white/10'
                        }`}
                      >
                        <div className={`text-sm font-medium transition-colors ${isSelected ? 'text-white' : 'text-zinc-200 group-hover:text-white'}`}>
                          {item.label}
                        </div>
                        {item.properties?.description && (
                           <div className={`text-[10px] mt-1 leading-relaxed line-clamp-2 italic ${isSelected ? 'text-white/80' : 'text-zinc-500'}`}>
                              {item.properties.description}
                           </div>
                        )}
                      </div>
                    );
                  })}
              </motion.div>
            );
          })
        )}
      </div>
      
      <div className="p-4 bg-black/40 border-t border-white/5">
         <div className="flex justify-between items-center text-[10px] uppercase font-bold tracking-tighter text-zinc-600">
            <span>Graph Health</span>
            <span className="text-meta-accent">Optimal</span>
         </div>
      </div>
    </div>
  );
};
