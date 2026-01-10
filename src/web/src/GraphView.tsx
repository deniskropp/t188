import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

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

interface GraphViewProps {
  nodes: Node[];
  edges: Edge[];
}

const GraphView: React.FC<GraphViewProps> = ({ nodes, edges }) => {
  const cyRef = useRef<HTMLDivElement>(null);
  const cyInstance = useRef<cytoscape.Core | null>(null);

  useEffect(() => {
    if (!cyRef.current) return;

    cyInstance.current = cytoscape({
      container: cyRef.current,
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'background-color': '#6366f1',
            'color': '#fff',
            'font-size': '10px',
            'font-family': 'Inter',
            'text-valign': 'center',
            'text-halign': 'center',
            'width': '40px',
            'height': '40px',
            'border-width': 2,
            'border-color': '#4f46e5',
            'overlay-opacity': 0,
          }
        },
        {
          selector: 'node[type="Character"]',
          style: { 'background-color': '#10b981', 'border-color': '#059669' }
        },
        {
          selector: 'node[type="Event"]',
          style: { 'background-color': '#f43f5e', 'border-color': '#e11d48' }
        },
        {
          selector: 'node[type="Location"]',
          style: { 'background-color': '#f59e0b', 'border-color': '#d97706' }
        },
        {
          selector: 'edge',
          style: {
            'label': 'data(label)',
            'width': 2,
            'line-color': '#475569',
            'target-arrow-color': '#475569',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'font-size': '8px',
            'text-background-color': '#0f172a',
            'text-background-opacity': 0.8,
            'color': '#94a3b8',
            'text-rotation': 'autorotate',
          }
        }
      ],
      elements: []
    });

    return () => {
      if (cyInstance.current) {
        cyInstance.current.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (!cyInstance.current) return;

    // Deduplicate nodes by ID
    const uniqueNodesMap = new Map();
    nodes.forEach(n => uniqueNodesMap.set(n.id, n));
    const uniqueNodes = Array.from(uniqueNodesMap.values());

    // Deduplicate edges by source-target-label
    const uniqueEdgesMap = new Map();
    edges.forEach(e => {
      const id = `${e.source}-${e.target}-${e.label}`;
      uniqueEdgesMap.set(id, { ...e, id });
    });
    const uniqueEdges = Array.from(uniqueEdgesMap.values());

    const elements = [
      ...uniqueNodes.map(n => ({ data: { ...n } })),
      ...uniqueEdges.map(e => ({ data: { ...e } }))
    ];

    cyInstance.current.elements().remove();
    cyInstance.current.add(elements);
    cyInstance.current.layout({ name: 'cose', animate: true }).run();
  }, [nodes, edges]);

  return <div id="cy" ref={cyRef} />;
};

export default GraphView;
