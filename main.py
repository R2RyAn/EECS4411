from BPlusTree import BPlusTree
if __name__ == "__main__":
    bpt = BPlusTree(max=4)
    keys = [10, 20, 5, 6, 12, 30, 7, 17]

    for key in keys:
        bpt.insert(key, f"Value-{key}")

    bpt.display_tree()

    print("\nSearch Results:")
    for key in keys:
        print(f"Key {key}: {bpt.search(key)}")

    print("Key 100 (not in tree):", bpt.search(100))