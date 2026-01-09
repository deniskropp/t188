import pytest
from src.shared.pipes import Pipe

def test_pipe_push_pull():
    p = Pipe[str]("test_pipe")
    assert p.is_empty
    
    p.push("hello")
    assert not p.is_empty
    
    val = p.pull()
    assert val == "hello"
    assert p.is_empty

def test_pipe_peek():
    p = Pipe[int]("int_pipe")
    p.push(42)
    
    assert p.peek() == 42
    assert not p.is_empty # Peek shouldn't remove
    
    val = p.pull()
    assert val == 42
    assert p.is_empty
