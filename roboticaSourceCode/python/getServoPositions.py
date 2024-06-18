import sys
from pyax12.connection import Connection
import RPi.GPIO as gpio

dyx_idElbow = 18
dyx_idBase = 2


#gripper rotate
sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

def getPosition():
    currentAngles = [0, 0]
    currentAngles[0] = sc.get_present_position(dyx_idBase)/1024 * 300 -150
    currentAngles[1] = sc.get_present_position(dyx_idElbow)/1024 * 300 -150
    return


getPosition()
