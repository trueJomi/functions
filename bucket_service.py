from firebase_admin import storage

bucket = storage.bucket()

def exist_file(file_name: str) -> bool:
    return bucket.blob(file_name).exists()