"""
Thread-safe bounded buffer for producer-consumer synchronization.
Uses Condition variables for wait/notify mechanism.
"""

# The SharedBuffer is a manually synchronized bounded buffer built on a deque and a Condition.
# I chose deque because it offers O(1) append/pop operations and gives me full control over synchronization, 
# unlike queue.Queue, which hides the locking internals.
# put() blocks when the buffer is full, and get() blocks when empty. 
# Both use condition.wait() and condition.notify_all() to coordinate producer and consumer threads.

from collections import deque
from threading import Condition

# Lock only gives me mutual exclusion

# Condition gives coordination (wait for state change)

class SharedBuffer:
    """
    Thread-safe bounded buffer using Condition variables.
    
    Implements classic blocking queue pattern:
    - Producers block when full
    - Consumers block when empty
    - FIFO ordering guaranteed
    """
    
    def __init__(self, max_size):
        """
        Initialize buffer with maximum capacity.
        
        Args:
            max_size: Maximum number of items buffer can hold
        """
        self.max_size = max_size
        self.buffer = deque()  # FIFO queue
        self.condition = Condition()  # For wait/notify synchronization

    def put(self, item):
        """
        Add item to buffer (blocks if full).
        
        Producer thread calls this. Will wait if buffer is at capacity,
        then wake up when consumer removes an item.
        
        Args:
            item: Data to add (can be None for poison pill)
        """
        with self.condition:  # Acquire lock
            # Wait while buffer is full
            while len(self.buffer) >= self.max_size:
                self.condition.wait()  # Release lock and sleep
            
            # Add item to end of queue
            self.buffer.append(item)
            
            # Wake up any waiting consumers
            self.condition.notify_all()

    def get(self):
        """
        Remove and return item from buffer (blocks if empty).
        
        Consumer thread calls this. Will wait if buffer is empty,
        then wake up when producer adds an item.
        
        Returns:
            Item from front of queue
        """
        with self.condition:  # Acquire lock
            # Wait while buffer is empty
            while len(self.buffer) == 0:
                self.condition.wait()  # Release lock and sleep
            
            # Remove item from front of queue (FIFO)
            item = self.buffer.popleft()
            
            # Wake up any waiting producers
            self.condition.notify_all()
            
            return item

    def snapshot(self):
        """Return current buffer contents (for debugging/testing)."""
        return list(self.buffer)

    def __len__(self):
        """Return current number of items in buffer."""
        return len(self.buffer)