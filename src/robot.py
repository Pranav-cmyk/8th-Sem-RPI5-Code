import os

from dotenv import load_dotenv
from pydobot import Dobot

load_dotenv()


class Robot:
    def __init__(self, port=os.getenv("port")):
        self.dobot = Dobot(port=port, verbose=True)

    def move(self, action: str, increment: int = 5):
        _, _, _, _, j1, j2, j3, j4 = self.dobot.pose()
        match action:
            case "forward":
                j2 = j2 + increment
            case "backward":
                j2 = j2 - increment
            case "left":
                j1 = j1 + increment
            case "right":
                j1 = j1 - increment
            case _:
                pass
        self.dobot._set_ptp_cmd(j1, j2, j3, j4, mode=4, wait=False)
