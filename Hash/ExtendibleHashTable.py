from DiskStorage import DiskStorage
from Bucket import Bucket

class ExtendibleHashTable:
    """Implements an extendible hashing-based index with disk storage."""

    def __init__(self, bucket_size=2):
        self.global_depth = 1  # Start with 2^1 = 2 directory entries
        self.bucket_size = bucket_size
        self.directory = [0, 1]  # Initial directory entries (pointing to 2 buckets)
        self.storage = DiskStorage()  # Persistent storage for buckets

        # Create and store empty buckets
        for bucket_id in self.directory:
            bucket = Bucket(bucket_id, bucket_size, local_depth=1)
            self.storage.save_bucket(bucket)

    def hash_function(self, key):
        """Simple hash function using modulo based on global depth."""
        return key % (2 ** self.global_depth)

    def search(self, key):
        """Searches for a key in the hash table."""
        index = self.hash_function(key)
        bucket_id = self.directory[index]
        bucket = self.storage.load_bucket(bucket_id)

        return bucket.search(key) if bucket else None

    def insert(self, key, value):
        """Inserts a key-value pair, handling bucket splits and directory growth."""
        index = self.hash_function(key)
        bucket_id = self.directory[index]
        bucket = self.storage.load_bucket(bucket_id)

        if key in bucket.keys:
            return False  # Duplicate key, do nothing

        if bucket.insert(key, value):
            self.storage.save_bucket(bucket)  # Save updated bucket
            return True

        # If bucket is full, split it
        self.split_bucket(index)
        return self.insert(key, value)  # Retry insertion after splitting

    def split_bucket(self, index):
        """Splits a bucket and updates the directory."""
        bucket_id = self.directory[index]
        old_bucket = self.storage.load_bucket(bucket_id)

        if old_bucket.local_depth == self.global_depth:
            self.double_directory()  # Expand directory if needed

        # Create a new bucket
        new_bucket_id = max(self.directory) + 1
        new_bucket = Bucket(new_bucket_id, self.bucket_size, old_bucket.local_depth + 1)

        # Increase local depth of old bucket
        old_bucket.local_depth += 1

        # Redistribute keys
        old_keys, old_values = old_bucket.keys[:], old_bucket.values[:]
        old_bucket.keys, old_bucket.values = [], []

        for i in range(len(old_keys)):
            target_bucket = old_bucket if self.hash_function(old_keys[i]) == bucket_id else new_bucket
            target_bucket.insert(old_keys[i], old_values[i])

        # Save updated buckets
        self.storage.save_bucket(old_bucket)
        self.storage.save_bucket(new_bucket)

        # Update directory
        hash_prefix = self.hash_function(old_keys[0])
        for i in range(len(self.directory)):
            if self.hash_function(i) == hash_prefix:
                self.directory[i] = new_bucket_id

    def double_directory(self):
        """Doubles the directory size when needed."""
        self.global_depth += 1
        self.directory.extend(self.directory)  # Duplicate entries

    def display(self):
        """Displays the directory and bucket contents."""
        print(f"\n🌐 Global Depth: {self.global_depth}")
        seen_buckets = set()
        for i, bucket_id in enumerate(self.directory):
            if bucket_id not in seen_buckets:
                seen_buckets.add(bucket_id)
                bucket = self.storage.load_bucket(bucket_id)
                print(f"Dir[{i:02b}] (Local Depth: {bucket.local_depth}): {list(zip(bucket.keys, bucket.values))}")

    def count_buckets(self):
        """Returns the number of unique buckets in the hash table."""
        return len(set(self.directory))  # Count unique bucket IDs


# Example Usage

