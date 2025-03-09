from BPlusTreeNode import BPlusTreeNode
class BPlusTree:
    def __init__(self, max=4):
        self.order = max
        self.root = BPlusTreeNode(max, is_leaf=True)

    def go_to_leaf(self, search_key):
        curr = self.root
        while not curr.is_leaf:
            i = 0
            while i < len(curr.keys) and search_key >= curr.keys[i]:
                i += 1
            curr = curr.children[i]
        return curr

    def search(self, search_key):

        leaf = self.go_to_leaf(search_key)
        for i, key in enumerate(leaf.keys):
            if key == search_key:
                return leaf.values[i]
        return None

    def insert(self, key, value):

        leaf = self.go_to_leaf(key)

        if key in leaf.keys:
            return False

        index = 0
        while index < len(leaf.keys) and leaf.keys[index] < key:
            index += 1
        leaf.keys.insert(index, key)
        leaf.values.insert(index, value)

        # Handle overflow (split if full)
        if leaf.is_full():
            self.handle_split(leaf)

        return True

    def handle_split(self, node):
        """Handles node splitting and parent updates."""
        new_node, promoted_key = node.split()

        # If the node is the root, create a new root
        if node == self.root:
            new_root = BPlusTreeNode(self.order, is_leaf=False)
            new_root.keys = [promoted_key]
            new_root.children = [node, new_node]
            node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
        else:
            # Insert the promoted key into the parent
            parent = node.parent
            index = 0
            while index < len(parent.keys) and parent.keys[index] < promoted_key:
                index += 1
            parent.keys.insert(index, promoted_key)
            parent.children.insert(index + 1, new_node)
            new_node.parent = parent

            # If parent is full, split again recursively
            if parent.is_full():
                self.handle_split(parent)

    def display_tree(self):
        """Displays the tree structure for debugging."""
        levels = []
        queue = [(self.root, 0)]
        while queue:
            node, level = queue.pop(0)
            if level >= len(levels):
                levels.append([])
            levels[level].append(node.keys)
            if not node.is_leaf:
                for child in node.children:
                    queue.append((child, level + 1))

        for i, level in enumerate(levels):
            print(f"Level {i}: {level}")

    def insert_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.isdigit():  # Ensure it's a valid number
                        key = int(line)
                        self.insert(key, f"Value-{key}")  # You can modify the value format if needed
            print(f"Inserted values from {filename} into the B+ Tree.")
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
