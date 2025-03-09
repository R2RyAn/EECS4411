from DiskStorage import DiskStorage
from Bucket import Bucket
import pickle

class ExtendibleHashTable:

    def __init__(self, bucket_size=2):
        # Create the disk storage object to start storing buckets to disk
        self.storage = DiskStorage()  # Persistent storage for buckets

        try:
            # Try to load in the metadata to create buckets
            with open("hash_metadata.pkl", "rb") as file:
                metadata = pickle.load(file)
                self.global_depth = metadata["global_depth"]
                self.directory = metadata["directory"]
                print("Previous hash table metadata loaded.")

        except FileNotFoundError:
            # If we havent found metadata
            print("No previous data found. Initializing new hash table.")
            self.global_depth = 1
            self.bucket_size = bucket_size
            self.directory = [0, 1]  # Initial directory entries (pointing to 2 buckets)

            # Create and store empty buckets
            for bucket_id in self.directory:
                bucket = Bucket(bucket_id, bucket_size, local_depth=1)
                self.storage.save_bucket(bucket)

        self.load_buckets()

    def hash_function(self, key):
        # Hash function using Pythons built-in hash function.
        return abs(hash(key)) % (2 ** 32) % (2 ** self.global_depth)

    def search(self, key):
        """Searches for a key in the hash table."""
        index = self.hash_function(key)
        # Bucket Id is what the hash function gives it
        bucket_id = self.directory[index]
        bucket = self.storage.load_bucket(bucket_id)
        return key in bucket.keys if bucket else None

    def insert(self, key):
        # Inserts a key while handling bucket splits and directory growth.
        index = self.hash_function(key)
        bucket_id = self.directory[index]
        bucket = self.storage.load_bucket(bucket_id)

        if key in bucket.keys:
            return False  # Duplicate key, do nothing

        if bucket.insert(key):  # If there's space, insert and return
            self.storage.save_bucket(bucket)
            return True

        # If bucket is full, split it
        self.split_bucket(index)
        return self.insert(key)  # Retry insertion after splitting

    def split_bucket(self, index):
        # Splits a bucket and updates the directory.
        bucket_id = self.directory[index]
        old_bucket = self.storage.load_bucket(bucket_id)

        if old_bucket.local_depth == self.global_depth:
            self.double_directory()

        # Create a new bucket
        new_bucket_id = max(self.directory) + 1
        new_bucket = Bucket(new_bucket_id, self.bucket_size, old_bucket.local_depth + 1)

        # Increase local depth of old bucket
        old_bucket.local_depth += 1

        # Redistribute keys
        old_keys = old_bucket.keys[:]
        old_bucket.keys = []

        for key in old_keys:
            if self.hash_function(key) & (1 << (old_bucket.local_depth - 1)):
                new_bucket.insert(key)
            else:
                old_bucket.insert(key)

        # Save updated buckets
        self.storage.save_bucket(old_bucket)
        self.storage.save_bucket(new_bucket)

        # Update directory
        for i in range(len(self.directory)):
            if self.directory[i] == bucket_id:
                if (i >> (old_bucket.local_depth - 1)) & 1:
                    self.directory[i] = new_bucket_id

        self.save_metadata()  # Ensure directory updates are saved

    def double_directory(self):
        # Doubles the directory size when needed.
        self.global_depth += 1
        new_directory = self.directory[:]
        self.directory.extend(new_directory)  # Duplicate entries
        self.save_metadata()  # Ensure directory updates are saved

    def display(self):
        # Displays the directory and bucket contents.
        print(f"\nGlobal Depth: {self.global_depth}")
        seen_buckets = set()
        for i, bucket_id in enumerate(self.directory):
            if bucket_id not in seen_buckets:
                seen_buckets.add(bucket_id)
                bucket = self.storage.load_bucket(bucket_id)
                print(f"Dir[{i:02b}] (Local Depth: {bucket.local_depth}): {bucket.keys}")

    def count_buckets(self):
        # Returns the number of unique buckets in the hash table.
        return len(set(self.directory))  # Count unique bucket IDs

    def save_metadata(self):
        # Stores metadata about the hash table.
        try:
            with open("hash_metadata.pkl", "wb") as f:
                pickle.dump({
                    "global_depth": self.global_depth,
                    "directory": self.directory
                }, f)
        except Exception as e:
            print(f"Failed to save metadata: {e}")

    def load_buckets(self):
        #Loads saved buckets from disk and restore buckets.
        try:
            # Load metadata first
            with open("hash_metadata.pkl", "rb") as f:
                metadata = pickle.load(f)
                self.global_depth = metadata["global_depth"]
                self.directory = metadata["directory"]

            bucket_ids = set(self.directory)  # Get all unique bucket IDs from the directory
            for bucket_id in bucket_ids:
                bucket = self.storage.load_bucket(bucket_id)
                if bucket:
                    print(f"Loaded Bucket-{bucket_id}: {bucket.keys} (Local Depth: {bucket.local_depth})")
                else:
                    print(f"Failed to load Bucket-{bucket_id}")

        except FileNotFoundError:
            print("No previous hash table metadata found. Starting fresh.")
        except Exception as e:
            print(f"Error loading buckets: {e}")

    # Function to insert values from a file
    def insert_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line.isdigit():  # Ensure it's a valid number
                        key = int(line)
                        self.insert(key)
            print(f"Inserted values from {filename} into the Extendible Hash Table.")
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except Exception as e:
            print(f"Error reading file: {e}")