import hashlib


def _get_hash(file, algorithm: str) -> str:
    """Returns file hash with the given algorithm

    Args:
        file: File to hash
        algorithm (str): Hashing algorithm name

    Returns:
        str: File hash in uppercase hexadecimal format
    """
    
    # Hashs the file
    file_hash = hashlib.file_digest(file, algorithm)
        
    # Converts the hash to hex
    file_hash = file_hash.hexdigest()
        
    # Put the hash in uppercase
    file_hash = file_hash.upper()
    
    # Return the hash
    return file_hash


def get_sha256(file_path: str) -> tuple[str, str]:
    """Get the sha256 hash of a file

    Args:
        file_path (str): File path location

    Returns:
        tuple[str, str]: Tuple (algorithm, file hash)
    """
    
    # Opens the file as binary file
    with open(file_path, 'rb', buffering=0) as file:
        # Get the file hash
        file_hash = _get_hash(file, 'sha256')
        
        # Retuns a tuple (algorithm, file hash)
        return ('sha256', file_hash)
    
    
def get_md5(file_path: str) -> tuple[str, str]:
    """Get the md5 hash of a file

    Args:
        file_path (str): File path location

    Returns:
        tuple[str, str]: Tuple (algorithm, file hash)
    """
    
    # Opens the file as binary file
    with open(file_path, 'rb', buffering=0) as f:
        # Get the file hash
        file_hash = _get_hash(f, 'md5')
        
        # Retuns a tuple (algorithm, file hash)
        return ('md5', file_hash)
    
    
def get_both(file_path: str) -> list[tuple[str, str]]:
    """Get both sha256 and md5 hashes of a file
    
    Args:
        file_path (str): File path location

    Returns:
        list[tuple[str, str]]: List of file hashes tuple (algorithm, file hash)
    """
    
    # Opens the file as binary file
    with open(file_path, 'rb', buffering=0) as file:
        
        # Retuns a list with both tuple (algorithm, file hash)
        return [
            ('sha256', _get_hash(file, 'sha256')),
            ('md5', _get_hash(file, 'md5')),
        ]
    
    
def get_all(file_path: str) -> list[tuple[str, str]]:
    """Get all hashes of a file

    Args:
        file_path (str): File path location

    Returns:
        list[tuple[str, str]]: List of file hashes tuple (algorithm, file hash)
    """    
    
    # List of all the file hashes
    hash_list: list = []
    
    # Opens the file as binary file
    with open(file_path, 'rb', buffering=0) as file:
        
        # Getting all possible file hashes
        for algo in hashlib.algorithms_available:
            try: hash_list.append(_get_hash(file, algo))
            except: continue
    
    # Sorting the list by algorithm name
    hash_list.sort(key = lambda key: key[0])
    
    # Returns the list of hashes tuples (algorithm, file hash)
    return hash_list


def list_algorithms() -> list[str]:
    """Return a sorted list of all the available algorithms

    Returns:
        list: Sorted list of all the available algorithms
    """
    
    # Removing brocken algo from hashlib available algorithms
    algo_list = [item for item in hashlib.algorithms_available if not item.startswith('shake_')]
    
    # Returns the sorted by name list of algorithm
    return sorted(algo_list)