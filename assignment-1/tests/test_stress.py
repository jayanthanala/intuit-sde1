"""Stress tests: high volume and randomized timing to verify robustness."""

import random
import time
from src.container import SourceContainer, DestinationContainer
from src.shared_buff import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer


def test_large_volume():
    """Test with 300 items to verify no data loss under high volume."""
    data = list(range(300))
    source = SourceContainer(data.copy())
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=5)

    p = Producer(source, buffer)
    c = Consumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == data


def test_randomized_jitter():
    """Test with random delays to simulate unpredictable real-world timing."""
    data = list(range(100))
    source = SourceContainer(data.copy())
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=3)

    # Override Producer with random sleep to simulate variable processing speed
    class JitterProducer(Producer):
        def run(self):
            while True:
                item = self.source.read_next()
                if item is None:
                    self.buffer.put(None)
                    break
                time.sleep(random.random() * 0.005)
                self.buffer.put(item)

    # Override Consumer with random sleep to simulate variable processing speed
    class JitterConsumer(Consumer):
        def run(self):
            while True:
                item = self.buffer.get()
                if item is None:
                    break
                time.sleep(random.random() * 0.005)
                self.destination.store(item)

    p = JitterProducer(source, buffer)
    c = JitterConsumer(buffer, dest)

    p.start(); c.start()
    p.join(); c.join()

    assert dest.items == data
