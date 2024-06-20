import sys
from pyax12.connection import Connection
import RPi.GPIO as gpio


#gripper rotate
sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

def getPosition(id):

    positionDegrees = sc.get_present_position(id, degrees=True)

    return positionDegrees

