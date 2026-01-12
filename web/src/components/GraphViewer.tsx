import React, { useMemo, useRef, useState, useEffect } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

interface Node {
  id: string;
  label: string;
  type: string;
  properties: any;
}

interface Edge {
  source: string;
  target: string;
  label: string;
}

interface GraphViewerProps {
  nodes: Node[];
  edges: Edge[];
  onNodeClick?: (nodeId: string) => void;
  selectedNodeId?: string | null;
}

const NODE_REL_SIZE = 6;

const typeColors: Record<string, string> = {
  'Character': '#fbbf24', // Yellow (Dopamin style)
  'Location': '#10b981', // Green
  'Event': '#f87171',    // Red (evt: style)
  'Concept': '#6366f1',  // Blue-Indigo
  'LatentPattern': '#8b5cf6', // Purple
  'DreamNarrative': '#d946ef', // Pink
  'ImplicitPlan': '#fb923c',   // Orange
};

const typePrefixes: Record<string, string> = {
  'Event': 'evt',
  'LatentPattern': 'pattern',
  'DreamNarrative': 'dream',
  'ImplicitPlan': 'plan',
  'Character': 'char',
  'Location': 'loc',
};


import { useTheme } from '../context/ThemeContext';

export const GraphViewer: React.FC<GraphViewerProps> = ({ nodes, edges, onNodeClick, selectedNodeId }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const { theme } = useTheme();

  useEffect(() => {
    if (!containerRef.current) return;

    const ro = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect;
      setDimensions({ width, height });
    });

    ro.observe(containerRef.current);
    return () => ro.disconnect();
  }, []);

  const gData = useMemo(() => {
    return {
      nodes: nodes.map(n => ({
        ...n,
        color: typeColors[n.type] || '#6366f1'
      })),
      links: edges.map(e => ({
        source: e.source,
        target: e.target,
        label: e.label
      }))
    };
  }, [nodes, edges]);

  const isDark = theme === 'dark';
  const highlightColor = isDark ? '#ffffff' : '#18181b';
  const labelBg = isDark ? 'rgba(10, 10, 12, 0.8)' : 'rgba(255, 255, 255, 0.9)';
  const linkColor = isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.1)';

  return (
    <div ref={containerRef} className="w-full h-full relative bg-meta-bg transition-colors duration-300">
      <div className="absolute top-6 left-6 z-10 pointer-events-none">
        <div className="flex items-center gap-3 px-4 py-2 bg-meta-surface/80 backdrop-blur-2xl border border-meta-border rounded-2xl shadow-2xl">
           <div className={`w-2 h-2 rounded-full ${nodes.length > 0 ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`} />
           <span className="text-[10px] font-black uppercase tracking-[0.2em] text-meta-muted italic">
             {nodes.length > 0 ? 'World Graph Live' : 'Awaiting Data'}
           </span>
        </div>
      </div>

      {nodes.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center p-8 bg-meta-surface/20 backdrop-blur-sm rounded-3xl border border-meta-border">
                <div className="text-meta-muted text-xs font-bold uppercase tracking-widest mb-2">No Active World State</div>
                <div className="text-meta-muted text-[10px]">Begin a narrative to generate the graph</div>
            </div>
          </div>
      )}
      
      {dimensions.width > 0 && (
        <ForceGraph2D
          width={dimensions.width}
          height={dimensions.height}
          graphData={gData}
          nodeLabel={(node: any) => `${node.type}: ${node.label}`}
          onNodeClick={(node: any) => onNodeClick?.(node.id)}
          linkDirectionalArrowLength={4}
          linkDirectionalArrowRelPos={1}
          linkCurvature={0.2}
          backgroundColor="rgba(0,0,0,0)"
          nodeRelSize={NODE_REL_SIZE}
          linkWidth={1.5}
          linkColor={() => linkColor}
          nodeCanvasObject={(node: any, ctx, globalScale) => {
            const isSelected = node.id === selectedNodeId;
            const prefix = typePrefixes[node.type];
            const label = prefix ? `${prefix}_${node.label.toLowerCase().replace(/\s+/g, '_')}` : node.label;
            const fontSize = 10 / globalScale;
            const color = node.color;

            // Shadow/Glow
            if (isSelected) {
              ctx.beginPath();
              ctx.arc(node.x, node.y, NODE_REL_SIZE * 2, 0, 2 * Math.PI, false);
              const gradient = ctx.createRadialGradient(node.x, node.y, NODE_REL_SIZE, node.x, node.y, NODE_REL_SIZE * 2.5);
              gradient.addColorStop(0, `${color}44`);
              gradient.addColorStop(1, 'rgba(0,0,0,0)');
              ctx.fillStyle = gradient;
              ctx.fill();
            }

            // Node core
            ctx.beginPath();
            ctx.arc(node.x, node.y, isSelected ? NODE_REL_SIZE * 1.5 : NODE_REL_SIZE, 0, 2 * Math.PI, false);
            ctx.fillStyle = isSelected ? highlightColor : color;
            ctx.fill();

            // Outer ring for selected
            if (isSelected) {
              ctx.strokeStyle = highlightColor;
              ctx.lineWidth = 2 / globalScale;
              ctx.stroke();
            }

            // Label Box
            ctx.font = `${fontSize}px Inter`;
            const textWidth = ctx.measureText(label).width;
            const padding = 4 / globalScale;
            const boxWidth = textWidth + padding * 2;
            const boxHeight = fontSize + padding;

            ctx.fillStyle = labelBg;
            ctx.beginPath();
            // ctx.roundRect(node.x - boxWidth / 2, node.y + NODE_REL_SIZE + padding, boxWidth, boxHeight, 4 / globalScale);
            // Standard rect for compatibility if roundRect is picky or not available in all envs
            ctx.rect(node.x - boxWidth / 2, node.y + NODE_REL_SIZE + padding, boxWidth, boxHeight);
            ctx.fill();
            
            ctx.strokeStyle = isSelected ? color : `${color}44`;
            ctx.lineWidth = 1 / globalScale;
            ctx.stroke();

            // Label Text
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = isSelected ? (isDark ? '#fff' : color) : (isDark ? color : '#18181b');
            // Actually, keep it simple: always colored text on light bg, or white on dark bg?
            // Let's rely on labelTextColor for selected, and keep normal logic for others
             ctx.fillStyle = isSelected ? (isDark ? '#fff' : color) : (isDark ? color : '#000');
            ctx.fillStyle = isSelected ? (isDark ? '#fff' : color) : color; 
             // Wait, if !isSelected, and light mode, `color` on `white bg` is visible.
             // If !isSelected, and dark mode, `color` on `dark bg` (label box) is visible.
             
             // Let's refine based on labelBg:
             // dark mode: labelBg is dark. color is bright (e.g. yellow). Text is visible.
             // light mode: labelBg is white. color is bright. Text might be hard to read if color is too light (like yellow).
             // But typeColors are: Yellow, Green, Red, Indigo, Purple, Pink, Orange. Most are ok on white, maybe yellow (#fbbf24) is a bit light.
             
             // Let's stick to simple logic:
             ctx.fillStyle = isSelected ? color : (isDark ? color : '#000');
             // If selected, we want it to pop.
             // If not selected, just the label.
             
             ctx.fillText(label, node.x, node.y + NODE_REL_SIZE + padding + boxHeight / 2);
          }}
        />
      )}
    </div>
  );
};
