import asyncio
from websocket_skyportal import SkyPortalWebSocketClient

cfg = {
        "host": "localhost",
        "port": 5000,
        "ssl": False,
        "token": "4d3c5e89-8f9f-40db-b9d9-69f4025275d2"
    }

async def main():
    client = SkyPortalWebSocketClient(cfg['host'], cfg['port'], cfg['ssl'], cfg['token'])
    await client.connect()
    while True:
            try:
                    content = await client.listen()
                    print(content + '\n')
            except Exception as e:
                    print(e)
                    break

if __name__ == "__main__":
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())