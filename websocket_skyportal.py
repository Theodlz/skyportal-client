import websockets
from api_skyportal import (
        api_skyportal,
        get_followup_request,
        get_obsplan,
)

class SkyPortalWebSocketClient:
        def __init__(self, host, port, ssl, skyportal_token):
                self.websocket_url = 'wss' if ssl == True else 'ws' + '://' + host + ':' + str(port) + '/websocket'
                self.api_url = 'https' if ssl == True else 'http' + '://' + host + ':' + str(port)

                self.api_token = skyportal_token
                self.websocket_token = None
                
                self.ws = None
        
        async def connect(self):
                print("Connecting to websocket server...")
                self.ws = await websockets.connect(self.websocket_url)

                response = api_skyportal("get", self.api_url, "/api/websocket_apps", token=self.api_token)
                if response.status_code != 200:
                        raise ValueError(f"Error: {response.status_code} {response.text}")
                self.websocket_token = response.json()['data']['token']

                await self.send(self.websocket_token)

                connected, attempts = False, 0
                while attempts < 5 and not connected:
                        msg = await self.recv()
                        if 'AUTH OK' in msg:
                                connected = True
                        elif "AUTH FAILED" in msg:
                                raise ValueError("Authentication failed")
                        else:
                                attempts += 1

                if not connected or attempts == 5:
                        raise ValueError("Connection failed")

                print("Connected to websocket server")     
                
        
        async def send(self, data):
                await self.ws.send(data)
        
        async def recv(self):
                if self.ws is None:
                        raise ValueError("Not connected")
                return await self.ws.recv()
        
        async def close(self):
                await self.ws.close()
        
        async def __aenter__(self):
                await self.connect()
                return self
        
        async def __aexit__(self, *args):
                await self.close()

        async def listen(self):
                # msg is a string, convert it to a dict if possible
                while True:
                # check the action type
                        msg = await self.recv()
                        try:
                                msg = eval(msg)
                        except:
                                if msg != "<3":
                                        raise ValueError(f"Message not supported: {msg}")
                        if type(msg) == dict:
                                if msg['actionType'] == 'skyportal/NEW_FOLLOWUP_REQUEST':
                                        payload = msg['payload']
                                        followup_request = get_followup_request(payload['request_id'], self.api_url, self.api_token)
                                        return {
                                                "type": "followup_request",
                                                "payload": followup_request
                                        }
                                elif msg['actionType'] == 'skyportal/NEW_OBSPLANS':
                                        payload = msg['payload']
                                        ids = payload['ids']
                                        obsplans = []
                                        for id in ids:
                                                obsplan = get_obsplan(id, self.api_url, self.api_token)
                                                obsplans.append(obsplan)
                                        return {
                                                "type": "obsplans",
                                                "payload": obsplans
                                        }
                                
      