class Node:
    def __init__(self, source, name, depth):
        self.source = source
        self.name = name
        self.depth = depth

    def __hash__(self):
        return hash(self.source)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.source == other.source
        return False