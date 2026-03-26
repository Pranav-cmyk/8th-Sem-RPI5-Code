import json
import os

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydobot import Dobot

app = FastAPI()
dobot = Dobot(port=os.environ.get("DobotPort", "/dev/ttyUSB0"), verbose=True)
x, y, z, r, j1, j2, j3, j4 = dobot.pose()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global x, y, z, r
    await websocket.accept()
    print(f"WebSocket Pi 4 connected from: {websocket.client.host}")
    try:
        while True:
            action = json.loads(await websocket.receive_text())
            print(f"Joystick Data: {action}")

            direction = action.get('direction')
            if direction == "Forward":
                dobot.move_to(x + 5, y, z, r, wait=False)
            elif direction == "Backward":
                dobot.move_to(x - 5, y, z, r, wait=False)
            elif direction == "Left":
                dobot.move_to(x, y - 5, z, r, wait=False)
            elif direction == "Right":
                dobot.move_to(x, y + 5, z, r, wait=False)

            x, y, z, r, j1, j2, j3, j4 = dobot.pose()

    except WebSocketDisconnect:
        print("Pi 4 Disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
