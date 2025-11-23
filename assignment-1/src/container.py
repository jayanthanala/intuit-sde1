# UPDATED: Now supports MULTIPLE threads accessing each container

# SourceContainer can be shared by multiple Producers - requires Lock
# DestinationContainer can be shared by multiple Consumers - requires Lock

# Thread-safe operations ensure no race conditions when multiple threads
# read from source or write to destination concurrently

from threading import Lock
from collections import deque


class SourceContainer:
    """
    Thread-safe container that supplies items one-by-one.
    Can be safely shared by multiple producer threads.
    """

    def __init__(self, items):
        """Initialize source container with items.
        
        Args:
            items: Iterable of items to process
            
        Raises:
            TypeError: If items is not iterable
        """
        try:
            # Use deque for O(1) popleft instead of list.pop(0) which is O(n)
            self.items = deque(items)
        except TypeError as e:
            raise TypeError(f"items must be iterable, got {type(items).__name__}: {e}")
        
        self.lock = Lock()  # Protect concurrent access

    def read_next(self):
        """Read next item from source (thread-safe).
        
        Returns:
            Next item or None if exhausted
        """
        with self.lock:  # Atomic read-and-remove
            if not self.items:
                return None  # Exhausted - each producer will get None once
            return self.items.popleft()  # O(1) FIFO


class DestinationContainer:
    """
    Thread-safe container that stores consumed items.
    Can be safely shared by multiple consumer threads.
    """

    def __init__(self):
        """Initialize empty destination container."""
        self.items = []
        self.lock = Lock()  # Protect concurrent writes

    def store(self, item):
        """Store item to destination (thread-safe).
        
        Args:
            item: Item to store
        """
        with self.lock:  # Atomic append
            self.items.append(item)
    
    def get_items(self):
        """Get all stored items (thread-safe read).
        
        Returns:
            Copy of items list
        """
        with self.lock:
            return list(self.items)


"""
If we changed the architecture so that multiple producers were pulling from the same SourceContainer, 
or multiple consumers were writing into the same DestinationContainer, those operations would become race conditions.

The fix is straightforward:

-> Add a threading.Lock() inside each container.

-> Wrap all modifying operations (pop, append, etc.) inside a with lock: block.
"""
