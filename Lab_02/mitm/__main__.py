import argparse
import aiohttp
from aiohttp import web
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_der_public_key, Encoding, PublicFormat
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from client.utils import wrap_json, unwrap_json


class APIError(Exception):
    pass


async def api_request(sess, url, method, data):
    async with sess.post(f"{url}/{method}", json=data) as resp:
        rj = await resp.json()
        if rj["status"] == "ok":
            return rj["result"]
        else:
            raise APIError(rj["result"])


async def start_session(req):
    url = f"http://{req.app['server_addr']}:{req.app['server_port']}/api"
    data = await req.json()
    print(data)
    mitm_private_key = ec.generate_private_key(ec.SECP256R1())
    mitm_public_key = mitm_private_key.public_key()
    mitm_public_key_bytes = mitm_public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    mitm_public_key_str = base64.b64encode(mitm_public_key_bytes).decode()
    client_public_key = load_der_public_key(base64.b64decode(data["pubkey"]))

    async with aiohttp.ClientSession() as sess:
        try:
            server_data = await api_request(sess, url, "session", {"pubkey": mitm_public_key_str})
        except APIError as e:
            return web.json_response({"status": "error", "result": str(e)})

    server_public_key = load_der_public_key(base64.b64decode(server_data["pubkey"]))
    
    m2c_key = mitm_private_key.exchange(ec.ECDH(), client_public_key)
    m2s_key = mitm_private_key.exchange(ec.ECDH(), server_public_key)
    m2c_kdf = HKDF(algorithm=hashes.SHA256(), length=16, salt=None, info=None)
    m2s_kdf = HKDF(algorithm=hashes.SHA256(), length=16, salt=None, info=None)
    req.app["db"][server_data["sid"]] = (m2c_kdf.derive(m2c_key), m2s_kdf.derive(m2s_key))

    server_data["pubkey"] = mitm_public_key_str
    return web.json_response({"status": "ok", "result": server_data})


async def method(req):
    url = f"http://{req.app['server_addr']}:{req.app['server_port']}/api"
    data = await req.json()
    sid = data["sid"]
    if sid in req.app["db"]:
        m2c_key, m2s_key = req.app["db"][sid]
        request = unwrap_json(data, m2c_key, sid)
        print(f"request: {request}")
        data = wrap_json(request, m2s_key, sid)
    async with aiohttp.ClientSession() as sess:
        try:
            server_data = await api_request(sess, url, req.match_info['method'], data)
        except APIError as e:
            return web.json_response({"status": "error", "result": str(e)})
    if sid in req.app["db"]:
        response = unwrap_json(server_data, m2s_key, sid)
        print(f"response: {response}")
        server_data = wrap_json(response, m2c_key, sid)
    return web.json_response({"status": "ok", "result": server_data})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        dest='address',
        help="server address",
        default='127.0.0.1',
    )
    parser.add_argument(
        '-p',
        dest='port',
        help="server port",
        type=int,
        default=9203,
    )
    parser.add_argument(
        '-m',
        dest='listen_port',
        help="mitm port",
        type=int,
        default=9204,
    )
    args = parser.parse_args()

    app = web.Application()
    app["db"] = {}
    app["server_addr"] = args.address
    app["server_port"] = args.port
    app.add_routes([
            web.post("/api/session", start_session),
            web.post("/api/{method}", method)
        ])
    web.run_app(app, port=args.listen_port)
