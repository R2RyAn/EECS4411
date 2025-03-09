import os
import pickle


class Bucket:
    """Represents a bucket in the extendible hash table."""

    def __init__(self, bucket_id, size=2, local_depth=1):
        self.bucket_id = bucket_id
        self.size = size  # Max number of keys per bucket
        self.local_depth = local_depth  # Number of bits used to index this bucket
        self.keys = []  # Keys stored in the bucket
        self.values = []  # Corresponding values

    def is_full(self):
        """Returns True if the bucket is full."""
        return len(self.keys) >= self.size

    def insert(self, key, value):
        """Inserts a key-value pair if not a duplicate."""
        if key in self.keys:
            return False  # Duplicate key, do nothing
        self.keys.append(key)
        self.values.append(value)
        return True

    def search(self, key):
        """Searches for a key and returns its value if found."""
        if key in self.keys:
            return self.values[self.keys.index(key)]
        return None  # Key not found

    def split(self):
        """Splits the bucket into two new buckets and returns them."""
        self.local_depth += 1  # Increase local depth when splitting
        new_bucket = Bucket(self.bucket_id + 1, self.size, self.local_depth)
        return new_bucket

    def serialize(self):
        """Returns a dictionary representation of the bucket."""
        return {
            "bucket_id": self.bucket_id,
            "size": self.size,
            "local_depth": self.local_depth,
            "keys": self.keys,
            "values": self.values
        }

    @staticmethod
    def deserialize(data):
        """Creates a Bucket instance from a dictionary."""
        bucket = Bucket(data["bucket_id"], data["size"], data["local_depth"])
        bucket.keys = data["keys"]
        bucket.values = data["values"]
        return bucket