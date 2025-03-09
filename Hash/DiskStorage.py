from Bucket import Bucket
import os
import pickle

class DiskStorage:


    def __init__(self, directory="hash_buckets"):
        # Manage the bucket storage on disk using Pickle
        self.directory = directory
        os.makedirs(directory, exist_ok=True)  # If it already exist dont create it

    def _get_filename(self, bucket_id):
        """Generates a file path for a given bucket."""
        return os.path.join(self.directory, f"bucket_{bucket_id}.pkl")

    def save_bucket(self, bucket):
        """Stores a bucket to disk."""
        with open(self._get_filename(bucket.bucket_id), 'wb') as f:
            pickle.dump(bucket.serialize(), f)

    def load_bucket(self, bucket_id):
        """Loads a bucket from disk."""
        try:
            with open(self._get_filename(bucket_id), 'rb') as f:
                return Bucket.deserialize(pickle.load(f))
        except FileNotFoundError:
            return None  # Bucket does not exist yet