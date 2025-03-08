import math
class BPlusTreeNode:
    def __init__(self, order = 4, is_leaf=False):
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.values = [] if is_leaf else None  # Only leaf nodes store values
        self.children = [] if not is_leaf else None  # Only internal nodes store child pointers
        self.next_leaf = None  # Only leaf nodes have next_leaf for range queries
        self.parent = None

    def is_full(self):
        return len(self.keys) >= self.order


    def split(self):
        mid = math.floor(len(self.keys) / 2)
        promoted = self.keys[mid]

        new_node = BPlusTreeNode(self.order, is_leaf=self.is_leaf)

        if self.is_leaf:

            new_node.keys = self.keys[mid:]
            new_node.values = self.values[mid:]
            self.keys = self.keys[:mid]
            self.values = self.values[:mid]
            new_node.next_leaf = self.next_leaf
            self.next_leaf = new_node
        else:
            new_node.keys = self.keys[mid + 1:]
            self.keys = self.keys[:mid]
            new_node.children = self.children[mid + 1:]
            self.children = self.children[:mid + 1]

            for child in new_node.children:
                child.parent = new_node

        new_node.parent = self.parent
        return new_node, promoted

