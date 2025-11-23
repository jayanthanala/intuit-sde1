"""Producer thread: reads from source container and writes to shared buffer."""

import threading
import time
import logging

class Producer(threading.Thread):
    """Continuously reads items from source and pushes to buffer until EOF (None)."""

    def __init__(self, source, buffer):
        super().__init__(name="Producer")
        self.source = source
        self.buffer = buffer

    def run(self):
        """Read items from source, put into buffer, send poison pill (None) when done."""
        try:
            while True:
                try:
                    item = self.source.read_next()
                    if item is None:  # End of data stream
                        logging.debug("Producer sending stop signal (None)")
                        self.buffer.put(None)  # Signal consumer to stop
                        break

                    self.buffer.put(item)  # Blocks if buffer is full
                    logging.debug(f"PUT {item} → Buffer: {self.buffer.snapshot()}")
                    time.sleep(0.05)
                    
                except AttributeError as e:
                    logging.error(f"Producer: Invalid source/buffer object: {e}")
                    raise
                except Exception as e:
                    logging.error(f"Producer: Error processing item: {e}")
                    # Send poison pill on error to prevent consumer deadlock
                    self.buffer.put(None)
                    raise
                    
        except Exception as e:
            logging.critical(f"Producer thread failed: {e}", exc_info=True)
            raise
