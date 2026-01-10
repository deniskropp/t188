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

    def get_summary(self, exclude_types: Optional[List[str]] = None) -> str:
        """Returns a string summary of all nodes and edges in the graph, with special handling for subconscious nodes."""
        if not self.graph.nodes:
            return "The world is currently empty."
            
        summary = ["Current World State:"]
        
        # Group Subconscious Nodes to handle them specially
        subconscious_sessions = []
        other_nodes = []
        
        for node_id, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'Unknown')
            if exclude_types and node_type in exclude_types:
                continue
                
            if node_type == "SubconsciousSession":
                # Try to get timestamp from id or properties
                session_time = 0
                if "_" in str(node_id):
                    try:
                        session_time = int(str(node_id).split("_")[-1])
                    except ValueError: pass
                subconscious_sessions.append((session_time, node_id, data))
            elif node_type in ["SubconsciousCue", "LatentPattern", "DreamNarrative", "ImplicitPlan"]:
                # These will be referenced by their sessions
                continue
            else:
                other_nodes.append((node_id, data))

        # Summarize Other Nodes
        if other_nodes:
            summary.append("Entities:")
            for node_id, data in other_nodes:
                node_type = data.get('type', 'Unknown')
                name = data.get('name') or data.get('description') or node_id
                summary.append(f"- [{node_type}] {name} (ID: {node_id})")
        
        # Summarize Subconscious History (Only latest in detail)
        if subconscious_sessions:
            subconscious_sessions.sort(key=lambda x: x[0], reverse=True)
            summary.append("\nSubconscious History:")
            
            # Latest session
            latest_time, latest_id, latest_data = subconscious_sessions[0]
            req = latest_data.get("request", "Unknown Request")
            summary.append(f"- LATEST SESSION: {req} (ID: {latest_id})")
            
            # Get related nodes for latest session
            for _, target, key, _ in self.graph.out_edges(latest_id, keys=True, data=True):
                target_data = self.graph.nodes[target]
                t_type = target_data.get("type", "Unknown")
                t_desc = target_data.get("description") or target_data.get("content") or target
                # Keep it concise
                if len(str(t_desc)) > 100:
                    t_desc = str(t_desc)[:100] + "..."
                summary.append(f"  * [{t_type}] {t_desc}")
            
            # Older sessions (just IDs/summaries)
            if len(subconscious_sessions) > 1:
                summary.append(f"- {len(subconscious_sessions)-1} Older subconscious sessions stored in graph.")

        # Summarize Edges (excluding subconscious ones to save space)
        if self.graph.edges:
            summary.append("\nRelationships:")
            edge_count = 0
            for source, target, key, data in self.graph.edges(keys=True, data=True):
                # Skip subconscious edges
                if "sub_session" in str(source):
                    continue
                summary.append(f"- {source} --({key})--> {target}")
                edge_count += 1
            if edge_count == 0 and self.graph.edges:
                summary.append("(Narrative relationships are stored but omitted from this summary)")
                
        return "\n".join(summary)

    def save_to_json(self, path: str):
        """Saves the graph to a JSON file."""
        import json
        data = nx.node_link_data(self.graph)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, path: str):
        """Loads the graph from a JSON file."""
        import json
        import os
        if not os.path.exists(path):
            return
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            self.graph = nx.node_link_graph(data)
        except Exception as e:
            print(f"Error loading graph from {path}: {e}")
            self.graph = nx.MultiDiGraph()
