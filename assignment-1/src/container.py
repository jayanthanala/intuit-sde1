class SourceContainer:
    """
    Simple container that supplies items one-by-one.
    """

    def __init__(self, items):
        self.items = list(items)

    def read_next(self):
        if not self.items:
            return None
        return self.items.pop(0)


class DestinationContainer:
    """
    Container that stores consumed items.
    """

    def __init__(self):
        self.items = []

    def store(self, item):
        self.items.append(item)
