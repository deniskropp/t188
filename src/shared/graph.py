import networkx as nx
from typing import List, Dict, Any, Optional
from src.shared.models import GraphNode, GraphEdge, KeyValue

class GraphStore:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_node(self, node: GraphNode):
        """Adds a node to the graph."""
        props = {kv.key: kv.value for kv in node.properties}
        self.graph.add_node(node.id, type=node.type, **props)

    def add_edge(self, edge: GraphEdge):
        """Adds an edge to the graph."""
        props = {kv.key: kv.value for kv in edge.properties}
        self.graph.add_edge(edge.source, edge.target, key=edge.relationship, **props)

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Retrieves a node by ID."""
        if not self.graph.has_node(node_id):
            return None
        data = self.graph.nodes[node_id]
        # Separate type from other properties
        properties = data.copy()
        node_type = properties.pop('type', 'Unknown')
        kv_list = [KeyValue(key=k, value=str(v)) for k, v in properties.items()]
        return GraphNode(id=node_id, type=node_type, properties=kv_list)

    def get_edges(self, source_id: str) -> List[GraphEdge]:
        """Retrieves all outgoing edges from a source node."""
        if not self.graph.has_node(source_id):
            return []
        
        edges = []
        for _, target, key, data in self.graph.out_edges(source_id, keys=True, data=True):
            kv_list = [KeyValue(key=k, value=str(v)) for k, v in data.items()]
            edges.append(GraphEdge(
                source=source_id,
                target=target,
                relationship=key,
                properties=kv_list
            ))
        return edges

    def query_subgraph(self, center_node_id: str, radius: int = 1) -> Dict[str, Any]:
        """Returns a subgraph around a node (for context injection)."""
        if not self.graph.has_node(center_node_id):
            return {"nodes": [], "edges": []}
            
        subgraph = nx.ego_graph(self.graph, center_node_id, radius=radius)
        return nx.node_link_data(subgraph)

    def clear(self):
        """Clears the graph (useful for testing)."""
        self.graph.clear()

    def get_summary(self) -> str:
        """Returns a string summary of all nodes and edges in the graph."""
        if not self.graph.nodes:
            return "The world is currently empty."
            
        summary = ["Current World State:"]
        
        # Summarize Nodes
        summary.append("Nodes:")
        for node_id, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'Unknown')
            name = data.get('name') or data.get('description') or node_id
            summary.append(f"- [{node_type}] {name} (ID: {node_id})")
            
        # Summarize Edges
        if self.graph.edges:
            summary.append("\nRelationships:")
            for source, target, key, data in self.graph.edges(keys=True, data=True):
                summary.append(f"- {source} --({key})--> {target}")
                
        return "\n".join(summary)
