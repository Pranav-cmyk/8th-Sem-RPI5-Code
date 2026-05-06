import json

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from src import Robot

app = FastAPI()
robot = Robot()


@app.websocket("/socket")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print(f"WebSocket Pi 4 connected from: {websocket.client.host}")
    try:
        while True:
            action = await websocket.receive_json()
            await websocket.send_text(f"Moving robot {action.get('action')}")
            robot.move(action.get("action"), 10)

    except WebSocketDisconnect:
        print("Pi 4 Disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
