from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from server.crypto.idea import do_encode, do_decode
import os
import json
import base64


def wrap_json(data, session_key, session_id):
    ret, iv = do_encode(data, session_key)
    rj = {"sid": session_id, "iv": base64.b64encode(iv).decode(), "data": base64.b64encode(ret).decode()}
    return rj


def unwrap_json(data, session_key, session_id):
    assert session_id == data["sid"]
    iv = base64.b64decode(data["iv"])
    data_enc = base64.b64decode(data["data"])
    data_bytes = do_decode(data_enc, session_key, iv)

    rj = json.loads(data_bytes)
    return rj


def encrypt(data, key):
    padder = PKCS7(64).padder()
    data_padded = padder.update(data.encode())
    data_padded += padder.finalize()

    iv = os.urandom(8)
    enc = Cipher(algorithms.IDEA(key), modes.CBC(iv)).encryptor()
    ret = iv + enc.update(data_padded)
    ret += enc.finalize()
    return base64.b64encode(ret).decode()


def decrypt(data, key):
    b = base64.b64decode(data)
    iv, data_enc = b[:8], b[8:]
    data_bytes = do_decode(data_enc, key, iv)
    return data_bytes.decode()