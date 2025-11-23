"""
Test cases for multiple producers and multiple consumers.

Validates thread-safe operation with concurrent producers/consumers:
- Multiple producers sharing same source
- Multiple consumers sharing same destination
- Correct item distribution and counting
- No data loss or duplication
- Proper termination with poison pills
"""
from src.container import SourceContainer, DestinationContainer
from src.shared_buff import SharedBuffer
from src.producer import Producer
from src.consumer import Consumer
import time


def test_two_producers_two_consumers():
    """Test 2 producers and 2 consumers working concurrently.
    
    Setup:
      - 2 producers sharing same source (20 items)
      - 2 consumers sharing same destination
      - Small buffer (size 3) to force blocking
    
    Expected:
      - All 20 items transferred exactly once
      - No duplicates, no missing items
      - Both consumers receive items (load balanced)
    """
    # Create shared source with 20 items
    items = list(range(1, 21))  # [1, 2, 3, ..., 20]
    source = SourceContainer(items)
    
    # Create shared destination
    dest = DestinationContainer()
    
    # Create small buffer to test blocking
    buffer = SharedBuffer(max_size=3)
    
    # Create 2 producers sharing the same source
    producer1 = Producer(source, buffer)
    producer2 = Producer(source, buffer)
    
    # Create 2 consumers sharing the same destination
    consumer1 = Consumer(buffer, dest)
    consumer2 = Consumer(buffer, dest)
    
    # Start all threads
    producer1.start()
    producer2.start()
    consumer1.start()
    consumer2.start()
    
    # Wait for all to complete
    producer1.join(timeout=10)
    producer2.join(timeout=10)
    consumer1.join(timeout=10)
    consumer2.join(timeout=10)
    
    # Verify all threads completed
    assert not producer1.is_alive(), "Producer 1 did not complete"
    assert not producer2.is_alive(), "Producer 2 did not complete"
    assert not consumer1.is_alive(), "Consumer 1 did not complete"
    assert not consumer2.is_alive(), "Consumer 2 did not complete"
    
    # Verify all items transferred
    result_items = dest.get_items()
    assert len(result_items) == 20, f"Expected 20 items, got {len(result_items)}"
    
    # Verify no duplicates (each item appears exactly once)
    assert sorted(result_items) == items, "Items mismatch or duplicates detected"


def test_three_producers_one_consumer():
    """Test 3 producers and 1 consumer.
    
    Setup:
      - 3 producers sharing same source (30 items)
      - 1 consumer
      - Buffer size 5
    
    Expected:
      - All 30 items transferred
      - Producers compete for items from source
      - Consumer processes all items
    """
    items = list(range(100, 130))  # [100, 101, ..., 129]
    source = SourceContainer(items)
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=5)
    
    # Create 3 producers
    producers = [Producer(source, buffer) for _ in range(3)]
    
    # Create 1 consumer
    consumer = Consumer(buffer, dest)
    
    # Start all
    for p in producers:
        p.start()
    consumer.start()
    
    # Wait for completion
    for p in producers:
        p.join(timeout=10)
        assert not p.is_alive(), "Producer did not complete"
    
    consumer.join(timeout=10)
    assert not consumer.is_alive(), "Consumer did not complete"
    
    # Verify results
    result_items = dest.get_items()
    assert len(result_items) == 30, f"Expected 30 items, got {len(result_items)}"
    assert sorted(result_items) == items, "Items mismatch"
  


def test_one_producer_three_consumers():
    """Test 1 producer and 3 consumers.
    
    Setup:
      - 1 producer
      - 3 consumers sharing same destination
      - Buffer size 4
    
    Expected:
      - All items transferred
      - Items distributed among consumers
      - No duplicates
    """
    items = list(range(200, 230))  # [200, 201, ..., 229]
    source = SourceContainer(items)
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=4)
    
    # Create 1 producer
    producer = Producer(source, buffer)
    
    # Create 3 consumers
    consumers = [Consumer(buffer, dest) for _ in range(3)]
    
    # Start all
    producer.start()
    for c in consumers:
        c.start()
    
    # Wait for completion
    producer.join(timeout=10)
    assert not producer.is_alive(), "Producer did not complete"
    
    for c in consumers:
        c.join(timeout=10)
        assert not c.is_alive(), "Consumer did not complete"
    
    # Verify results
    result_items = dest.get_items()
    assert len(result_items) == 30, f"Expected 30 items, got {len(result_items)}"
    assert sorted(result_items) == items, "Items mismatch"

def test_producer_consumer_ratios():
    """Test different producer:consumer ratios.
    
    Tests asymmetric configurations:
      - 4 producers, 2 consumers
      - 2 producers, 4 consumers
    
    Expected:
      - All items transferred regardless of ratio
      - System handles imbalance correctly
    """
    # Test 1: More producers than consumers
    items1 = list(range(2000, 2040))  # 40 items
    source1 = SourceContainer(items1)
    dest1 = DestinationContainer()
    buffer1 = SharedBuffer(max_size=3)
    
    producers1 = [Producer(source1, buffer1) for _ in range(4)]
    consumers1 = [Consumer(buffer1, dest1) for _ in range(2)]
    
    for t in producers1 + consumers1:
        t.start()
    for t in producers1 + consumers1:
        t.join(timeout=10)
    
    result1 = dest1.get_items()
    assert len(result1) == 40, f"4P+2C: Expected 40 items, got {len(result1)}"
    assert sorted(result1) == items1, "4P+2C: Items mismatch"
    
    # Test 2: More consumers than producers
    items2 = list(range(3000, 3040))  # 40 items
    source2 = SourceContainer(items2)
    dest2 = DestinationContainer()
    buffer2 = SharedBuffer(max_size=3)
    
    producers2 = [Producer(source2, buffer2) for _ in range(2)]
    consumers2 = [Consumer(buffer2, dest2) for _ in range(4)]
    
    for t in producers2 + consumers2:
        t.start()
    for t in producers2 + consumers2:
        t.join(timeout=10)
    
    result2 = dest2.get_items()
    assert len(result2) == 40, f"2P+4C: Expected 40 items, got {len(result2)}"
    assert sorted(result2) == items2, "2P+4C: Items mismatch"

def test_large_scale_multi_thread():
    """Large-scale test: 10 producers + 10 consumers with 500 items.
    
    Setup:
      - 10 producers sharing source
      - 10 consumers sharing destination
      - 500 items total
      - Buffer size 10
    
    Expected:
      - All 500 items transferred
      - No data loss under high concurrency
      - Reasonable completion time
    """
    items = list(range(5000, 5500))  # 500 items
    source = SourceContainer(items)
    dest = DestinationContainer()
    buffer = SharedBuffer(max_size=10)
    
    # Create 10 producers and 10 consumers
    producers = [Producer(source, buffer) for _ in range(10)]
    consumers = [Consumer(buffer, dest) for _ in range(10)]
    
    start_time = time.time()
    
    # Start all threads
    for p in producers:
        p.start()
    for c in consumers:
        c.start()
    
    # Wait for completion
    for p in producers:
        p.join(timeout=30)
        assert not p.is_alive(), "Producer timed out"
    
    for c in consumers:
        c.join(timeout=30)
        assert not c.is_alive(), "Consumer timed out"
    
    elapsed = time.time() - start_time
    
    # Verify results
    result_items = dest.get_items()
    assert len(result_items) == 500, f"Expected 500 items, got {len(result_items)}"
    assert sorted(result_items) == items, "Items mismatch in large-scale test"