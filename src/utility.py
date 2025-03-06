import json
import hashlib

def json_read(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def json_write(data, path):
    with open(path, "w") as f:
        json.dump(data, f)

def calculate_checksum(file_path, algorithm="sha256", chunk_size=8192):
    """
    Calculate checksum (hash) of a file.
    # Example usage
    file_path = "example.txt"
    md5_checksum = calculate_checksum(file_path, "md5")
    sha1_checksum = calculate_checksum(file_path, "sha1")
    sha256_checksum = calculate_checksum(file_path, "sha256")


    parameter file_path (str, path_like)
    parameter algorithm (str) algorithm hash
    parameter chunk_size (int) chunk size
    Returns hash value
    """
    hash_func = hashlib.new(algorithm)  # Create hash object (md5, sha1, sha256, etc.)

    try:
        with open(file_path, "rb") as f:  # Open file in binary mode
            while chunk := f.read(chunk_size):  # Read in chunks (memory efficient)
                hash_func.update(chunk)  # Update hash with file data
    except (PermissionError, OSError):
        return None
    return hash_func.hexdigest()  # Return hexadecimal checksum

