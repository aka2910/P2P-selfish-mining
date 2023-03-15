class Node:
    def __init__(self, block, timestamp):
        # The timestamp is the time at which the block was received
        self.block = block
        self.timestamp = timestamp

        self.children = [] # List of nodes that are children of this node