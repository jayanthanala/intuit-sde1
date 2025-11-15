"""Test buffer edge cases: extreme sizes and boundary conditions."""

from src.container import SourceContainer, DestinationContainer
from src.shared_buff import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer


def test_buffer_size_one():
    """Test strict alternation with buffer size of 1 (tightest synchronization)."""
    source = SourceContainer([10, 20, 30])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=1)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == [10, 20, 30]


def test_buffer_larger_than_data():
    """Test that large buffer doesn't cause issues when data is smaller."""
    source = SourceContainer([1, 2, 3])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=10)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == [1, 2, 3]
