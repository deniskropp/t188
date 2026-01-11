import React, { useMemo } from 'react';
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

export const GraphViewer: React.FC<GraphViewerProps> = ({ nodes, edges, onNodeClick, selectedNodeId }) => {
  const gData = useMemo(() => {
    return {
      nodes: nodes.map(n => {
        const isSelected = n.id === selectedNodeId;
        return {
          ...n,
          val: isSelected ? 20 : 10,
          // Color coding by type
          color: n.type === 'Character' ? '#fbbf24' : 
                 n.type === 'Location' ? '#10b981' : 
                 n.type === 'Event' ? '#f87171' : 
                 n.type.includes('Subconscious') ? '#8b5cf6' : '#6366f1'
        };
      }),
      links: edges.map(e => ({
        source: e.source,
        target: e.target,
        label: e.label
      }))
    };
  }, [nodes, edges, selectedNodeId]);

  return (
    <div className="glass rounded-2xl overflow-hidden w-full h-full relative min-h-[400px]">
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-2">
        <h2 className="text-sm font-bold text-white bg-black/40 px-3 py-1 rounded-full backdrop-blur-md border border-white/10 flex items-center gap-2">
           <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
           World Graph Live
        </h2>
      </div>
      <ForceGraph2D
        graphData={gData}
        nodeLabel={(node: any) => `${node.type}: ${node.label}`}
        nodeAutoColorBy="type"
        onNodeClick={(node: any) => onNodeClick?.(node.id)}
        linkDirectionalArrowLength={3.5}
        linkDirectionalArrowRelPos={1}
        linkCurvature={0.25}
        linkLabel="label"
        backgroundColor="rgba(0,0,0,0)"
        nodeRelSize={6}
        linkWidth={(link: any) => {
           const isRelatedToSelection = selectedNodeId && (link.source.id === selectedNodeId || link.target.id === selectedNodeId);
           return isRelatedToSelection ? 3 : 1;
        }}
        linkColor={(link: any) => {
           const isRelatedToSelection = selectedNodeId && (link.source.id === selectedNodeId || link.target.id === selectedNodeId);
           return isRelatedToSelection ? 'rgba(139, 92, 246, 0.5)' : 'rgba(255,255,255,0.1)';
        }}
        nodeCanvasObject={(node: any, ctx, globalScale) => {
          const label = node.label;
          const fontSize = 12 / globalScale;
          const isSelected = node.id === selectedNodeId;
          
          ctx.font = `${isSelected ? 'bold ' : ''}${fontSize}px Inter`;
          const textWidth = ctx.measureText(label).width;
          const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.4); 

          if (isSelected) {
            ctx.beginPath();
            ctx.arc(node.x, node.y, nodeRelSize * 1.5, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba(139, 92, 246, 0.3)';
            ctx.fill();
            ctx.strokeStyle = '#8b5cf6';
            ctx.lineWidth = 2 / globalScale;
            ctx.stroke();
          }

          ctx.fillStyle = 'rgba(10, 10, 12, 0.9)';
          ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - nodeRelSize - bckgDimensions[1] - 2, bckgDimensions[0], bckgDimensions[1]);

          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillStyle = isSelected ? '#fff' : node.color;
          ctx.fillText(label, node.x, node.y - nodeRelSize - bckgDimensions[1] / 2 - 2);

          ctx.fillStyle = node.color;
          ctx.beginPath(); ctx.arc(node.x, node.y, isSelected ? nodeRelSize * 1.2 : nodeRelSize, 0, 2 * Math.PI, false); ctx.fill();
        }}
      />
    </div>
  );
};
