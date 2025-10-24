# src/presentation/websockets/websocket_server.py

from socketio import AsyncServer

# Socket.IO server
sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# 1-1 chat events
@sio.event
async def connect(sid, environ):
    """Client connected."""
    print(f"[socket] connected sid={sid}")
    await sio.emit("connected", {"sid": sid}, room=sid)

@sio.event
async def disconnect(sid):
    """Client disconnected."""
    print(f"[socket] disconnect sid={sid}")

@sio.on("ping")
async def handle_ping(sid, data):
    """Optional ping/pong."""
    print(f"[socket] ping received: {data}")
    await sio.emit("pong", {"received": data}, room=sid)

@sio.on("send_message")
async def send_message(sid, data: dict):
    """
    1-1 chat message.
    data = {
        "to": "<receiver_sid>",
        "message": "Hello!"
    }
    """
    receiver_sid = data.get("to")
    message = data.get("message")
    if receiver_sid and message:
        await sio.emit("receive_message", {"from": sid, "message": message}, room=receiver_sid)
        print(f"[socket] message from {sid} -> {receiver_sid}: {message}")