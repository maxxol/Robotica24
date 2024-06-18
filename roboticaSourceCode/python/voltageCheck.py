import sys
from pyax12.connection import Connection
import RPi.GPIO as gpio

dyx_idBase = 2 #arbitrary servo, just need one and this one is the first in 


#gripper rotate
sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

def getVoltage():
    #check voltage

	#if bad: sudoshutdown shell file
	#if knop: sudoshutdown shell file
    return


getPosition()
