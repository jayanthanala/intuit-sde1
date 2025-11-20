"""Consumer thread: reads from shared buffer and writes to destination container."""

import threading
import time
import logging

class Consumer(threading.Thread):
    """Continuously retrieves items from buffer and stores to destination until poison pill."""

    def __init__(self, buffer, destination):
        super().__init__(name="Consumer")
        self.buffer = buffer
        self.destination = destination

    def run(self):
        """Get items from buffer, store to destination, stop on poison pill (None)."""
        while True:
            # consumer bascially polls for new data in the queue
            item = self.buffer.get()  # Blocks if buffer is empty

            if item is None:  # Poison pill received
                logging.debug("Consumer received stop signal, exiting.")
                break

            self.destination.store(item)
            logging.debug(f"GOT {item} → Buffer: {self.buffer.snapshot()}")

            time.sleep(0.09)
