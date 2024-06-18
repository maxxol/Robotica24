import sys
from pyax12.connection import Connection
import RPi.GPIO as gpio
import subprocess

dyx_idBase = 2 #arbitrary servo, just need one and this one is the first in 
shutdown_script = "../shell/shutdown.sh"

#gripper rotate
sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

#gpio shutdown
shutdown_pin = 30 #does not exist, just a placeholder

voltage_tolerance = 2

def getVoltage(dyx_idBase):
    #check voltage
    current_voltage = sc.get_present_voltage(dyx_idBase)

    max_voltage = sc.get_max_voltage(dyx_idBase)
    min_voltage = sc.get_min_voltage(dyx_idBase)

	#if bad: sudoshutdown shell file
    if (current_voltage >  max_voltage - voltage_tolerance) or (current_voltage < min_voltage + voltage_tolerance):
        shutdown()

	#if knop: sudoshutdown shell file
    state = gpio.input(shutdown_pin)
    if state:
        shutdown()


def shutdown():
    sub_proc = subprocess.Popen(shutdown_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    


getVoltage()
