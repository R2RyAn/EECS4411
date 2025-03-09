from ExtendibleHashTable import ExtendibleHashTable

if __name__ == "__main__":
    eht = ExtendibleHashTable(bucket_size=2)

    print("\n🔄 Inserting keys into the Extendible Hash Table from 'values.txt'...")
    eht.insert_from_file("values.txt")

    eht.display()  # Show directory and buckets
    print("\nTotal Buckets:", eht.count_buckets())

    # === TEST LOADING FROM DISK ===
    print("\n🔁 Reloading Buckets from Disk to Verify Persistence...")
    eht.load_buckets()

    print("\n✅ Finished testing Extendible Hashing persistence.")
