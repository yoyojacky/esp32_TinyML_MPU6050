import asyncio, websockets, socket, re

UDP_IP = ''          # 监听所有网卡
UDP_PORT = 3000
WS_PORT  = 8765      # 浏览器连 ws://ip:8765

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(False)

CLIENTS = set()

async def udp_to_ws():
    global CLIENTS
    loop = asyncio.get_event_loop()
    while True:
        data = await loop.sock_recv(sock, 1024)
        data = data.decode().strip()
        if re.match(r'Y-?\d+\.\d+P-?\d+\.\d+R-?\d+\.\d+', data):
            dead = set()
            for ws in CLIENTS:
                try: await ws.send(data)
                except Exception: dead.add(ws)
            CLIENTS -= dead

async def handler(websocket):
    CLIENTS.add(websocket)
    await websocket.wait_closed()
    CLIENTS.remove(websocket)

async def main():
    await asyncio.gather(
        udp_to_ws(),
        websockets.serve(handler, '0.0.0.0', WS_PORT)
    )

asyncio.run(main())
