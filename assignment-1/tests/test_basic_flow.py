"""Test basic producer-consumer flow with simple data transfer."""

from src.container import SourceContainer, DestinationContainer
from src.shared_buff import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer


def test_transfer_all_items():
    """Verify all items are transferred from source to destination."""
    source = SourceContainer([1, 2, 3])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=2)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == [1, 2, 3]


def test_no_items():
    """Verify graceful handling when source container is empty."""
    source = SourceContainer([])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=2)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == []
