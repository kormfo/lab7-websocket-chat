from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uvicorn
import json
from datetime import datetime
from models import ChatMessage

app = FastAPI()

html_path = Path(__file__).parent / "templates"
app.mount("/static", StaticFiles(directory=html_path), name="static")

clients = {}


@app.get("/")
async def get():
    html = (html_path / "chat.html").read_text(encoding="utf-8")
    return HTMLResponse(content=html, status_code=200, media_type="text/html; charset=utf-8")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str = Query(None)):
    if not username or not username.strip():
        await websocket.close(code=4000, reason="Username is required")
        return

    username = username.strip()
    await websocket.accept()
    clients[username] = websocket

    join_msg = {
        "type": "system",
        "text": f"{username} joined",
        "online": len(clients),
        "ts": datetime.now().isoformat()
    }
    for client in clients.values():
        await client.send_text(json.dumps(join_msg))

    try:
        while True:
            data = await websocket.receive_text()

            try:
                json_data = json.loads(data)
            except json.JSONDecodeError:
                error_msg = {"type": "error", "detail": "Invalid JSON format"}
                await websocket.send_text(json.dumps(error_msg))
                continue

            try:
                validated = ChatMessage(**json_data)
            except Exception as e:
                error_msg = {"type": "error", "detail": str(e)}
                await websocket.send_text(json.dumps(error_msg))
                continue

            text = validated.text

            if text.startswith("/w "):
                parts = text[3:].split(" ", 1)
                if len(parts) < 2:
                    error_msg = {"type": "error", "detail": "Format: /w username message"}
                    await websocket.send_text(json.dumps(error_msg))
                    continue

                target_user, private_text = parts[0], parts[1]

                if target_user not in clients:
                    error_msg = {"type": "error", "detail": f"User '{target_user}' is not online"}
                    await websocket.send_text(json.dumps(error_msg))
                    continue

                private_msg = {
                    "type": "private",
                    "from": username,
                    "to": target_user,
                    "text": private_text,
                    "ts": datetime.now().isoformat()
                }
                await clients[target_user].send_text(json.dumps(private_msg))
                await websocket.send_text(json.dumps(private_msg))
                continue

            msg = {
                "type": "message",
                "user": username,
                "text": text,
                "ts": datetime.now().isoformat()
            }
            for client_name, client in clients.items():
                if client != websocket:
                    await client.send_text(json.dumps(msg))

    except WebSocketDisconnect:
        del clients[username]

        leave_msg = {
            "type": "system",
            "text": f"{username} left",
            "online": len(clients),
            "ts": datetime.now().isoformat()
        }
        for client in clients.values():
            await client.send_text(json.dumps(leave_msg))


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)