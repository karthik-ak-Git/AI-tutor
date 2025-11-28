"""
Tests for service classes
"""
import pytest
import os
from app.services.memory import SimpleMemory


def test_memory_add_messages():
    """Test adding messages to memory."""
    memory = SimpleMemory()
    memory.add_user_message("session1", "Hello")
    memory.add_ai_message("session1", "Hi there!")
    
    messages = memory.get_messages("session1")
    assert len(messages) == 2
    assert messages[0].content == "Hello"
    assert messages[1].content == "Hi there!"


def test_memory_clear_session():
    """Test clearing a session from memory."""
    memory = SimpleMemory()
    memory.add_user_message("session1", "Hello")
    memory.clear_session("session1")
    
    messages = memory.get_messages("session1")
    assert len(messages) == 0


def test_memory_multiple_sessions():
    """Test memory with multiple sessions."""
    memory = SimpleMemory()
    memory.add_user_message("session1", "Hello 1")
    memory.add_user_message("session2", "Hello 2")
    
    messages1 = memory.get_messages("session1")
    messages2 = memory.get_messages("session2")
    
    assert len(messages1) == 1
    assert len(messages2) == 1
    assert messages1[0].content == "Hello 1"
    assert messages2[0].content == "Hello 2"


def test_memory_get_last_n():
    """Test getting last N messages."""
    memory = SimpleMemory()
    for i in range(5):
        memory.add_user_message("session1", f"Message {i}")
    
    messages = memory.get_messages("session1", last_n=3)
    assert len(messages) == 3
    assert messages[0].content == "Message 2"
    assert messages[2].content == "Message 4"

