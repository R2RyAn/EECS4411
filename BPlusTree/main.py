from BPlusTree import BPlusTree
if __name__ == "__main__":
    bpt = BPlusTree(4)
    bpt.insert_from_file("values")
    bpt.display_tree()
