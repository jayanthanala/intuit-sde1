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
    try:
        # Setup: source with data, empty destination, buffer with capacity of 2
        source = SourceContainer([1234,2345,3456,4567,5678,6789])
        dest = DestinationContainer() #this is empty
        buffer = SharedBuffer(max_size=2) #let's assume we have a buzzer size of 2, so our dequque can only hold 2 items max.

        # Create producer and consumer threads
        producer = Producer(source, buffer)
        consumer = Consumer(buffer, dest)

        # Start both threads (run concurrently)
        producer.start()
        consumer.start()

        # Wait for both threads to complete
        producer.join(timeout=30.0)  # 30 second timeout
        consumer.join(timeout=30.0)

        # Check if threads are still alive (indicates timeout/deadlock)
        if producer.is_alive() or consumer.is_alive():
            logging.error("Threads did not complete within timeout - possible deadlock")
            raise RuntimeError("Producer-consumer threads timed out")

        print("Final destination:", dest.get_items())
        logging.info("Demo completed successfully")
        
    except ValueError as e:
        logging.error(f"Invalid configuration: {e}")
        raise
    except RuntimeError as e:
        logging.error(f"Runtime error during execution: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in run_demo: {e}", exc_info=True)
        raise


def run_multi_demo():
    """Demonstrate multiple producers and consumers working together.
    
    Shows:
      - 2 producers sharing same source
      - 2 consumers sharing same destination
      - Thread-safe concurrent operation
    """
    try:
        logging.info("Starting multi-producer multi-consumer demo")
        
        # Create shared resources
        items = list(range(1, 21))  # 20 items
        source = SourceContainer(items)
        dest = DestinationContainer()
        buffer = SharedBuffer(max_size=3)
        
        # Create 2 producers sharing the same source
        producer1 = Producer(source, buffer)
        producer2 = Producer(source, buffer)
        
        # Create 2 consumers sharing the same destination
        consumer1 = Consumer(buffer, dest)
        consumer2 = Consumer(buffer, dest)
        
        # Start all threads
        logging.info("Starting 2 producers and 2 consumers...")
        producer1.start()
        producer2.start()
        consumer1.start()
        consumer2.start()
        
        # Wait for all to complete
        producer1.join(timeout=30.0)
        producer2.join(timeout=30.0)
        consumer1.join(timeout=30.0)
        consumer2.join(timeout=30.0)
        
        # Check completion
        if any(t.is_alive() for t in [producer1, producer2, consumer1, consumer2]):
            logging.error("Some threads did not complete within timeout")
            raise RuntimeError("Multi-threaded demo timed out")
        
        # Display results
        result = dest.get_items()
        print(f"\nMulti-Producer Multi-Consumer Demo:")
        print(f"  Items produced: {items}")
        print(f"  Items consumed: {sorted(result)}")
        print(f"  Total items: {len(result)}")
        print(f"  All items transferred correctly: {sorted(result) == sorted(items)}")
        
        logging.info("Multi-demo completed successfully")
        
    except Exception as e:
        logging.error(f"Error in multi-demo: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    import sys
    
    try:
        # Run single producer-consumer demo
        print("="*60)
        print("SINGLE PRODUCER-CONSUMER DEMO")
        print("="*60)
        run_demo()
        
        print("\n" + "="*60)
        print("MULTI PRODUCER-CONSUMER DEMO")
        print("="*60)
        run_multi_demo()
        
    except Exception as e:
        logging.critical(f"Application failed: {e}")
        sys.exit(1)
