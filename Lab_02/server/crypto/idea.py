import json
import os
import base64

from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encode(data, session_key, sid):
    ret, iv = do_encode(data, session_key)

    return {
        'sid': sid,
        'iv': base64.b64encode(iv).decode(),
        'data': base64.b64encode(ret).decode(),
    }


def do_encode(data, session_key):
    data_bytes = json.dumps(data).encode()

    padder = PKCS7(64).padder()
    data_padded = padder.update(data_bytes)
    data_padded += padder.finalize()

    iv = os.urandom(8)
    enc = Cipher(algorithms.IDEA(session_key), modes.CBC(iv)).encryptor()
    ret = enc.update(data_padded)
    ret += enc.finalize()
    return ret, iv


def decode(data, session_key):
    iv = base64.b64decode(data["iv"])
    data_enc = base64.b64decode(data["data"])
    data_bytes = do_decode(data_enc, session_key, iv)
    
    return json.loads(data_bytes)


def do_decode(data_enc, session_key, iv):
    dec = Cipher(algorithms.IDEA(session_key), modes.CBC(iv)).decryptor()
    data_padded = dec.update(data_enc)
    data_padded += dec.finalize()

    padder = PKCS7(64).unpadder()
    data_bytes = padder.update(data_padded)
    data_bytes += padder.finalize()
    return data_bytes