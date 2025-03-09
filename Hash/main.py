from ExtendibleHashTable import ExtendibleHashTable
if __name__ == "__main__":
    eht = ExtendibleHashTable(bucket_size=2)
    keys = [12, 44, 32, 23, 56, 89, 9, 77, 99, 100]

    print("\n🔄 Inserting keys into the Extendible Hash Table...")
    for key in keys:
        eht.insert(key, f"Value-{key}")

    eht.display()  # Show directory and buckets
    print("\nTotal Buckets:", eht.count_buckets())

    print("\n🔍 Search Results:")
    for key in keys:
        print(f"Key {key}: {eht.search(key)}")

    print("\n❌ Key 200 (not in table):", eht.search(200))  # Should return None