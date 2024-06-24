from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()


connections: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket) 
    try:
        while True:
            data = await websocket.receive_text()
            client_port = websocket.client.port
            for connection in connections:
                if connection == websocket:
                    await connection.send_text(f"Voce :({client_port}) enviou: {data}")
                else:
                    await connection.send_text(f"Cliente :({client_port}) enviou: {data}")
    finally:
        connections.remove(websocket) 
