from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import load_der_public_key, Encoding, PublicFormat

import base64


ELLIPTIC_CURVE = ec.SECP256R1


def generate_keys():
    priv = ec.generate_private_key(ELLIPTIC_CURVE())
    pub = priv.public_key()
    return pub, priv


def generate_shared_key(priv, pub):
    return priv.exchange(ec.ECDH(), pub)


def generate_session_key(shared_key):
    return HKDF(algorithm=hashes.SHA256(), length=16, salt=None, info=None).derive(shared_key)


def b64enc(key):
    b = key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    return base64.b64encode(b).decode()


def b64dec(key):
    return load_der_public_key(base64.b64decode(key))
