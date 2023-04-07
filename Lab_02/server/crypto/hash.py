from cryptography.hazmat.primitives import hashes

import os
import base64


def hash(data, salt=None):
    if not salt:
        salt = os.urandom(8)
    h = hashes.Hash(hashes.SHA256())
    h.update(data.encode())
    h.update(salt)
    return h.finalize(), salt
    

def decode(data, salt):
    salt = b64bin(salt)
    data = b64bin(data)
    return data, salt


def b64str(data):
    return base64.b64encode(data).decode()


def b64bin(data):
    return base64.b64decode(data.encode('UTF-8'))
