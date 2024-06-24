from fastapi import FastAPI, WebSocket
from typing import List
import redis

app = FastAPI()

connections: List[WebSocket] = []

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def save_message(chat_id, message):
    redis_client.rpush(chat_id, message)

def get_messages(chat_id):
    return redis_client.lrange(chat_id, 0, -1)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    
    chat_id = "chat:global"  
    message_history = get_messages(chat_id)
    for message in message_history:
        await websocket.send_text(f"Historico: {message}")
    
    try:
        while True:
            data = await websocket.receive_text()
            client_port = websocket.client.port
            full_message = f"Cliente ({client_port}) enviou: {data}"
            

            save_message(chat_id, full_message)
            
            for connection in connections:
                if connection == websocket:
                    await connection.send_text(f"Voce ({client_port}) enviou: {data}")
                else:
                    await connection.send_text(full_message)
    finally:
        connections.remove(websocket)


save_message(chat_id, message)

messages = get_messages(chat_id)
print(messages)
