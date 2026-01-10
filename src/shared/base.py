from typing import Any, Type, TypeVar, Generic
from pydantic import BaseModel
from src.shared.graph import GraphStore
from src.shared.llm import LLMService, get_llm_service

T = TypeVar("T", bound=BaseModel)

class BaseRole:
    """Base class for all core roles in the MetaCognito system."""
    
    def __init__(self, graph_store: GraphStore, llm_service: LLMService | None = None):
        self.graph_store = graph_store
        self._llm = llm_service

    @property
    def llm(self) -> LLMService:
        if self._llm is None:
            self._llm = get_llm_service()
        return self._llm

    async def _generate_text(self, prompt: str) -> str:
        """Helper to generate plain text from the LLM."""
        return await self.llm.generate_text(prompt)

    async def _generate_structured(self, prompt: str, response_model: Type[T]) -> T:
        """Helper to generate structured output from the LLM."""
        return await self.llm.generate_structured(prompt, response_model)

    def _sync_nodes(self, nodes: list[Any]) -> None:
        """Sync a list of nodes with the graph store."""
        for node in nodes:
            self.graph_store.add_node(node)

    def _sync_edges(self, edges: list[Any]) -> None:
        """Sync a list of edges with the graph store."""
        for edge in edges:
            self.graph_store.add_edge(edge)
