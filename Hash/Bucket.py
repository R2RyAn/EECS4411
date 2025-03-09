import pickle
import os


class Bucket:
    """Represents a bucket in the extendible hash table."""

    def __init__(self, bucket_id, size=2, local_depth=1):
        self.bucket_id = bucket_id
        self.size = size  # Maximum keys per bucket
        self.local_depth = local_depth  # Local depth of this bucket
        self.keys = []  # Stores the keys

    def is_full(self):
        """Returns True if the bucket is full."""
        return len(self.keys) >= self.size

    def insert(self, key):
        """Inserts a key if it's not a duplicate."""
        if key in self.keys:
            return False  # Duplicate keys not allowed
        if self.is_full():
            return False
        self.keys.append(key)
        return True

    def search(self, key):
        """Checks if a key exists in the bucket."""
        return key in self.keys

    def split(self):
        """Splits the bucket and returns a new one."""
        self.local_depth += 1  # Increase local depth on split
        new_bucket = Bucket(self.bucket_id + 1, self.size, self.local_depth)
        return new_bucket

    def serialize(self):
        """Stores only keys and metadata for disk storage."""
        return {"bucket_id": self.bucket_id, "size": self.size, "local_depth": self.local_depth, "keys": self.keys}

    @staticmethod
    def deserialize(data):
        """Restores a bucket from saved data."""
        bucket = Bucket(data["bucket_id"], data["size"], data["local_depth"])
        bucket.keys = data["keys"]
        return bucket
