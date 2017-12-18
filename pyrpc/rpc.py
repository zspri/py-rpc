import asyncio
import websockets, aiohttp
import uuid
import json

class NoRpcServer(Exception):
    pass

class Image:
    def __init__(key, text=None, large=True):
        self.key = key
        self.text = text
        self.large = large

class RpcClient:
    def __init__(self, client_id, token, port = 6463, ver = 1):
        self.cid = client_id
        self.port = port
        self.ver = ver
        self.uri = "ws://127.0.0.1:{}?v={}&client_id={}&=encoding=json".format(self.port, self.ver, self.cid)
        print(self.uri)
        self.token = token
        self.aioses = aiohttp.ClientSession()

    async def authenticate(self):
        # https://discordapp.com/developers/docs/topics/rpc#authenticate
        payload = {
            "nonce": str(uuid.uuid4()),
            "args": {
                "access_token": self.token,
            },
            "cmd": "AUTHENTICATE"
        }
        res = None
        async with websockets.connect(self.uri) as ws:
            ws.send(payload)
            raw_res = await ws.recv()
            res = json.loads(raw_res)
            await ws.close()
        # https://discordapp.com/developers/docs/topics/rpc#authorize
        payload = {
            "nonce": str(uuid.uuid4()),
            "args": {
                "client_id": self.cid,
                "scopes": ["rpc.api", "rpc", "identity"],
                "rpc_origins": ["http://localhost:3436"]
            },
            "cmd": "AUTHORIZE"
        }
        res = None
        async with websockets.connect(self.uri) as ws:
            ws.send(payload)
            raw_res = await ws.recv()
            res = json.loads(raw_res)
            await ws.close()
        async with self.aioses as s:
            another_payload = {
                'client_id': self.cid,
                'client_secret': self.token,
                'grant_type': 'authorization_code',
                'code': res['data']['code']
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            async with session.post("https://discordapp.com/api/oauth2/token/rpc", data=json.dumps(another_payload), header=headers) as s:
                print(s.headers())
                print("-"*5)
                print(s.text())
