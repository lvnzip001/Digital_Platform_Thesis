import hashlib
from PIL import Image

def get_hash (file_location):
    """ Function to get the sha256 of any fiile
        Inputs: File location of object"""
    with open(file_location, "rb") as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes).hexdigest()
        return(hash)
