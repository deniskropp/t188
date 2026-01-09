import pytest
import asyncio
from src.shared.graph import GraphStore

@pytest.fixture(scope="function")
def graph_store():
    store = GraphStore()
    yield store
    store.clear()
