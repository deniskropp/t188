import React, { useEffect, useRef, useState, useMemo } from 'react';
import cytoscape from 'cytoscape';
import { 
  ZoomIn, 
  ZoomOut, 
  Maximize, 
  RefreshCw, 
  Search, 
  X, 
  Info,
  User,
  MapPin,
  Calendar,
  Box,
  Lightbulb
} from 'lucide-react';

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
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  // Sanitization helper
  const sanitizeLabel = (label: string) => {
    if (!label) return '';
    return label
      .replace(/^(itm:|loc:|chr:|con:|evt:|node:)/i, '')
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  // Icon mapping for node types
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'Character': return <User size={14} />;
      case 'Location': return <MapPin size={14} />;
      case 'Event': return <Calendar size={14} />;
      case 'Item': return <Box size={14} />;
      case 'Concept': return <Lightbulb size={14} />;
      default: return <Info size={14} />;
    }
  };

  useEffect(() => {
    if (!cyRef.current) return;

    cyInstance.current = cytoscape({
      container: cyRef.current,
      style: [
        {
          selector: 'node',
          style: {
            'label': (ele: any) => sanitizeLabel(ele.data('label')),
            'background-color': '#6366f1',
            'color': '#fff',
            'font-size': '10px',
            'font-family': 'Inter',
            'text-valign': 'center',
            'text-halign': 'center',
            'width': '46px',
            'height': '46px',
            'border-width': 2,
            'border-color': '#4f46e5',
            'overlay-opacity': 0,
            'transition-property': 'background-color, border-color, border-width, width, height',
            'transition-duration': 300,
            'text-wrap': 'wrap',
            'text-max-width': '80px',
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
          selector: 'node[type="Item"]',
          style: { 'background-color': '#8b5cf6', 'border-color': '#7c3aed' }
        },
        {
          selector: 'node[type="Concept"]',
          style: { 'background-color': '#06b6d4', 'border-color': '#0891b2' }
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 4,
            'border-color': '#fff',
            'width': '52px',
            'height': '52px',
          }
        },
        {
          selector: 'node.highlighted',
          style: {
            'border-width': 6,
            'border-color': '#fbbf24',
          }
        },
        {
          selector: 'edge',
          style: {
            'label': 'data(label)',
            'width': 2,
            'line-color': 'rgba(71, 85, 105, 0.4)',
            'target-arrow-color': 'rgba(71, 85, 105, 0.4)',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'font-size': '10px',
            'text-background-color': '#0f172a',
            'text-background-opacity': 0.8,
            'color': '#cbd5e1',
            'text-rotation': 'autorotate',
            'text-margin-y': -10,
            'text-outline-width': 1,
            'text-outline-color': '#0f172a',
          }
        }
      ],
      elements: [],
      userZoomingEnabled: true,
      userPanningEnabled: true,
    });

    cyInstance.current.on('tap', 'node', (evt) => {
      const nodeData = evt.target.data();
      setSelectedNode(nodeData);
    });

    cyInstance.current.on('tap', (evt) => {
      if (evt.target === cyInstance.current) {
        setSelectedNode(null);
      }
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
    cyInstance.current.layout({ 
      name: 'cose', 
      animate: true,
      nodeOverlap: 20,
      refresh: 20,
      fit: true,
      padding: 50,
      randomize: false,
      componentSpacing: 100,
      nodeRepulsion: 400000,
      edgeElasticity: 100,
      nestingFactor: 5,
      gravity: 80,
      numIter: 1000,
      initialTemp: 200,
      coolingFactor: 0.95,
      minTemp: 1.0
    }).run();
  }, [nodes, edges]);

  // Handle Search
  useEffect(() => {
    if (!cyInstance.current) return;
    
    cyInstance.current.nodes().removeClass('highlighted');
    
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      const matched = cyInstance.current.nodes().filter(node => {
        const rawLabel = node.data('label').toLowerCase();
        const cleanLabel = sanitizeLabel(node.data('label')).toLowerCase();
        const type = node.data('type').toLowerCase();
        return rawLabel.includes(query) || cleanLabel.includes(query) || type.includes(query);
      });
      
      matched.addClass('highlighted');
      if (matched.length > 0) {
        cyInstance.current.animate({
          center: { eles: matched },
          zoom: 1.2,
          duration: 500
        });
      }
    }
  }, [searchQuery]);

  const handleZoomIn = () => cyInstance.current?.zoom(cyInstance.current.zoom() * 1.2);
  const handleZoomOut = () => cyInstance.current?.zoom(cyInstance.current.zoom() * 0.8);
  const handleFit = () => cyInstance.current?.fit(undefined, 50);
  const handleRefreshLayout = () => cyInstance.current?.layout({ name: 'cose', animate: true }).run();

  return (
    <div className="graph-viewport">
      <div className="search-box">
        <Search className="search-icon" size={16} />
        <input 
          type="text" 
          className="search-input" 
          placeholder="Search entities..." 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div className="graph-toolbar">
        <button className="toolbar-btn" onClick={handleZoomIn} title="Zoom In"><ZoomIn size={18} /></button>
        <button className="toolbar-btn" onClick={handleZoomOut} title="Zoom Out"><ZoomOut size={18} /></button>
        <div className="toolbar-divider" />
        <button className="toolbar-btn" onClick={handleFit} title="Fit to Screen"><Maximize size={18} /></button>
        <button className="toolbar-btn" onClick={handleRefreshLayout} title="Refresh Layout"><RefreshCw size={18} /></button>
      </div>

      {selectedNode && (
        <div className="graph-details-panel">
          <div className="details-header">
            <div className="details-title">Entity Details</div>
            <button className="close-btn" onClick={() => setSelectedNode(null)}>
              <X size={16} />
            </button>
          </div>
          <div className="details-content">
            <div className="detail-row">
              <span className="detail-label">Name</span>
              <div className="detail-value" style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--primary)' }}>
                {sanitizeLabel(selectedNode.label)}
              </div>
              <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                ID: {selectedNode.id}
              </div>
            </div>
            <div className="detail-row">
              <span className="detail-label">Type</span>
              <div className="detail-value" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                {getTypeIcon(selectedNode.type)}
                {selectedNode.type}
              </div>
            </div>
            {selectedNode.properties && Object.keys(selectedNode.properties).length > 0 && (
              <div className="detail-row">
                <span className="detail-label">Properties</span>
                <div className="detail-value">
                  {Object.entries(selectedNode.properties).map(([key, val]) => (
                    <div key={key} style={{ marginBottom: '8px' }}>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '2px' }}>{key}</div>
                      <div style={{ background: 'rgba(255,255,255,0.03)', padding: '6px', borderRadius: '6px' }}>
                        {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      <div id="cy" ref={cyRef} />
    </div>
  );
};

export default GraphView;
