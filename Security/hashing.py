import hashlib

def make_hashes(password):
    """ Method to parse the passwords w highest hashing"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    """ Method to verify that the hsahing works """
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False