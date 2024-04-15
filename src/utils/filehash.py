import hashlib


def get_hash(file_path: str, algorithm: str) -> str:
    """Returns file hash with the given algorithm

    Args:
        file_path (str): File path location
        algorithm (str): Hashing algorithm name

    Returns:
        str: File hash in uppercase hexadecimal format
    """
    
    # Opens the file as binary file
    with open(file_path, 'rb') as file:
        # Hashs the file
        file_hash = hashlib.file_digest(file, algorithm)
            
        # Converts the hash to hex
        file_hash = file_hash.hexdigest()
            
        # Put the hash in uppercase
        file_hash = file_hash.upper()
        
        # Return the hash
        return file_hash


def list_algorithms() -> list[str]:
    """Return a sorted list of all the available algorithms

    Returns:
        list: Sorted list of all the available algorithms
    """
    
    # Removing brocken algo from hashlib available algorithms
    algo_list = [item for item in hashlib.algorithms_available if not item.startswith('shake_')]
    
    # Returns the sorted by name list of algorithm
    return sorted(algo_list)