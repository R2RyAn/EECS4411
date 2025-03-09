import pickle
import os


class Bucket:

    def __init__(self, bucket_id, size=2, local_depth=1):
        # Representing one bucket in the hash table
        self.bucket_id = bucket_id
        self.size = size  # Maximum keys per bucket
        self.local_depth = local_depth  # Local depth of this bucket
        self.keys = []  # Array to store the keys

    def is_full(self):
        # Returns True if the bucket is full.
        return len(self.keys) >= self.size

    def insert(self, key):
        # Boolean method that returns whether its possible to add the key or not
        if key in self.keys:
            return False  # Duplicate keys not allowed
        if self.is_full():
            return False  # Must split bucket to do so
        self.keys.append(key)
        return True

    def search(self, key):
        # Checks if key is in the bucket
        return key in self.keys

    def split(self):
        # Splits the bucket, by making a new one, incrementing the id and returning it
        self.local_depth += 1  # Increase local depth on split
        new_bucket = Bucket(self.bucket_id + 1, self.size, self.local_depth)
        return new_bucket

    def serialize(self):
        # Stores the key attributes of each bucket as metadata for disk reloading
        return {"bucket_id": self.bucket_id, "size": self.size, "local_depth": self.local_depth, "keys": self.keys}

    @staticmethod
    def deserialize(data):
        # Turns a saved bucket from metadata to actual in memory bucket
        bucket = Bucket(data["bucket_id"], data["size"], data["local_depth"])
        bucket.keys = data["keys"]
        return bucket
