"""Test FIFO ordering guarantee and poison pill shutdown mechanism."""

from src.container import SourceContainer, DestinationContainer
from src.shared_buff import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer


def test_order_preserved():
    """Verify items arrive in exact FIFO order (no reordering)."""
    source = SourceContainer([5, 4, 3, 2, 1])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=3)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == [5, 4, 3, 2, 1]


def test_poison_pill_not_stored():
    """Verify poison pill (None) is not stored in destination."""
    source = SourceContainer([7, 8])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=2)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert None not in dest.items
