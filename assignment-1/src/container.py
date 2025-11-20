# Only ONE thread ever touches each container

# SourceContainer is read only and accessed only by the Producer.

# DestinationContainer is written only by the Consumer.

# So there is no shared access, and therefore no race condition. No lock is required

class SourceContainer:
    """
    Simple container that supplies items one-by-one.
    """

    def __init__(self, items):
        self.items = list(items) # i could use a dequeue here to make it more optimized

    def read_next(self):
        if not self.items: 
            return None # the pill comes from here
        return self.items.pop(0) #FIFO


class DestinationContainer:
    """
    Container that stores consumed items.
    """

    def __init__(self):
        self.items = []

    def store(self, item):
        self.items.append(item)


"""
If we changed the architecture so that multiple producers were pulling from the same SourceContainer, 
or multiple consumers were writing into the same DestinationContainer, those operations would become race conditions.

The fix is straightforward:

-> Add a threading.Lock() inside each container.

-> Wrap all modifying operations (pop, append, etc.) inside a with lock: block.
"""
