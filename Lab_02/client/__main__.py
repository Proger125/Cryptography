from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import load_der_public_key, Encoding, PublicFormat
import argparse
import asyncio
import aiohttp
import base64
import os
from requests import ApiRequests, APIError


def get_client_keys():
    client_private_key = ec.generate_private_key(ec.SECP256R1())
    client_public_key = client_private_key.public_key()
    client_public_key_bytes = client_public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    client_public_key_str = base64.b64encode(client_public_key_bytes).decode()
    return client_private_key, client_public_key_str


def print_actions_menu():
    print("Choose an action:")
    print("0 Test session")
    print("1 Login")
    print("2 Register")
    print("3 Get file")
    print("4 Put file")
    print("5 Delete file")
    print("6 Exit")


async def main(args):
    url = f"http://{args.address}:{args.port}/api"
    async with aiohttp.ClientSession() as session:
        requests = ApiRequests(session, url)
        client_private_key, client_public_key = get_client_keys()
        data = await requests.api_request("session", {"pubkey": client_public_key})
        server_public_key = load_der_public_key(base64.b64decode(data["pubkey"]))
        shared_key = client_private_key.exchange(ec.ECDH(), server_public_key)

        session_key = HKDF(algorithm=hashes.SHA256(), length=16, salt=None, info=None).derive(shared_key)
        session_id = data["sid"]
        requests.set_session_key(session_key)
        requests.set_session_id(session_id)
        session_expiry = data["exp"]
        print(f"session {session_id}, expires {session_expiry}, session key {session_key}")
        while True:
            print_actions_menu()
            action = input()
            try:
                action = int(action)
                if action > 6 or action < 0:
                    raise ValueError
            except ValueError:
                print("Invalid action, please try another")
                continue
            
            try:
                if action == 0:
                    await requests.test_session(args.key)
                elif action == 1:
                    await requests.login()
                elif action == 2:
                    await requests.register()
                elif action == 3:
                    await requests.get_file(args.key)
                elif action == 4:
                    await requests.put_file(args.key)
                elif action == 5:
                    await requests.delete_file()
                elif action == 6:
                    break
                else:
                    print("Not implemented")
            except APIError as e:
                print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        dest='address',
        help="server address",
        default='127.0.0.1',
    )
    parser.add_argument(
        "-p",
        dest='port',
        help="server port",
        type=int,
        default=9203,
    )
    parser.add_argument(
        "-f",
        dest='keyfile',
        help="path to file containing 128-bit IDEA key (will be created from urandom if does not exist)",
        nargs="?",
        default='pk.key',
    )
    args = parser.parse_args()
    if args.keyfile is not None:
        if not os.path.isfile(args.keyfile):
            print("generating new keyfile")
            with open(args.keyfile, "wb") as f:
                f.write(os.urandom(16))
        with open(args.keyfile, "rb") as f:
            args.key = f.read()
            assert len(args.key) == 16
    else:
        args.key = None
    asyncio.run(main(args))
