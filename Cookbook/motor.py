from time import sleep

from pydobot import Dobot

# from adafruit_servokit import ServoKit

dobot = Dobot(port="/dev/ttyUSB0", verbose=True)
x, y, z, r, j1, j2, j3, j4 = dobot.pose()
dobot.move_to(x - 50, y, z, r, wait=True)


# kit = ServoKit(channels=16)
# kit.servo[0].angle = 0
# sleep(1)
