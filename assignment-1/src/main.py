"""Main entry point: demonstrates producer-consumer pattern with bounded buffer."""

import logging
from src.container import SourceContainer, DestinationContainer
from src.shared_buff import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer

# Configure logging to show thread activity and timing
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] %(message)s",
    datefmt="%H:%M:%S"
)

def run_demo():
    """Run producer-consumer demo: transfer items from source to destination via bounded buffer."""
    # Setup: source with data, empty destination, buffer with capacity of 2
    source = SourceContainer([1, 2, 3, 4, 5])
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=2)

    # Create producer and consumer threads
    producer = Producer(source, buffer)
    consumer = Consumer(buffer, dest)

    # Start both threads (run concurrently)
    producer.start()
    consumer.start()

    # Wait for both threads to complete
    producer.join()
    consumer.join()

    print("Final destination:", dest.items)

if __name__ == "__main__":
    run_demo()
