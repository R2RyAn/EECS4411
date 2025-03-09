from BPlusTreeNode import BPlusTreeNode

class BPlusTree:
    # Constructor, Max order of a tree is 4 by default, and root is a BPlussTreeNode
    def __init__(self, max=4):
        self.order = max
        # Root is a leaf node by default
        self.root = BPlusTreeNode(max, is_leaf=True)

    # Function to go to the leaf node
    def go_to_leaf(self, search_key):
        curr = self.root
        # while the current node is not a leaf
        while not curr.is_leaf:
            # i represent which child to go to
            i = 0
            while i < len(curr.keys) and search_key >= curr.keys[i]:
                i += 1
            curr = curr.children[i]
        return curr

    # Function to search for a key
    def search(self, search_key):
        # Call upon the go_to_leaf function to reach the correct leaf node to go to
        leaf = self.go_to_leaf(search_key)
        # Iterate through the keys in the leaf node
        for i, key in enumerate(leaf.keys):
            if key == search_key:
                return leaf.values[i]
        # If the key is not found, return None
        return None

    # Function to insert a key and value into the B+ Tree
    def insert(self, key, value):
        # Call upon the go_to_leaf function to reach the correct leaf node to go to
        leaf = self.go_to_leaf(key)

        # If the key is already in the leaf node, return False to avoid duplicates
        if key in leaf.keys:
            return False
        # Insert the key and value into the leaf node
        index = 0
        # Find the correct index to insert the key and value
        while index < len(leaf.keys) and leaf.keys[index] < key:
            index += 1
        leaf.keys.insert(index, key)
        leaf.values.insert(index, value)

        # Handle overflow
        if leaf.is_full():
            self.handle_split(leaf)

        return True

    # Function to handle overflow, handle the split of a node
    def handle_split(self, node):

        # Split the node using the split function from BPlusTreeNode
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

    # Display the tree in the command line
    def display_tree(self):
        count = 0
        levels = []
        queue = [(self.root, 0)]
        while queue:
            node, level = queue.pop(0)
            if level >= len(levels):
                levels.append([])
            levels[level].append(node.keys)
            count += 1
            if not node.is_leaf:
                for child in node.children:
                    queue.append((child, level + 1))

        for i, level in enumerate(levels):
            print(f"Level {i}: {level}")
        print(f"Number of nodes: {count}")

    # Function to insert values from a file
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
