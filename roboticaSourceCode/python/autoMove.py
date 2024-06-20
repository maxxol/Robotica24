import math
import numpy as np
from pyax12.connection import Connection
import RPi.GPIO as gpio

# Constants
# DEGREES_TO_RADIANS = math.pi / 180.0  # Multiplication factor to turn degree values into radian values
SERVO_BASE = 2
SERVO_ELBOW = 18
L_HUMERUS = 40.5  # Length of the humerus in units (cm)
L_ULNA = 32.0  # Length of the ulna in units 32 (cm)
L_CAM = 20.0  # Distance from elbow joint to camera on ulna in units (cm)
H_CAM = 43.0  # Height of the camera from the ground in units (cm)

"""
				ROBOT ASCII FOR VARIABLE EXPLANATION

			   base		   elbow	  camera	|  
				O--------------O-----------[]---O gripperbase
				|   humerus		 ulna			|
				|							   /\  gripper
				|
				|
			  __|__

			O = joint
			-,| = solid
			[] = special component
"""

SC = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)


"""
    Function that calculates the end-effector coordinate based on provided angles according to this formula:

    X = L1 * cos(angle1) + L2 * cos(angle1 + angle2) + L3 * cos(angle1 + angle2 + angle3) ...
    Y = L1 * sin(angle1) + L2 * sin(angle1 + angle2) + L3 * sin(angle1 + angle2 + angle3) ...

    Each angle is relative to the previous angle NOT relative to the x-axis (except for angle1)
"""
def forward_kinematics(lengths, angles):
    if len(lengths) != len(angles):
        print(f"Mismatch in lengths and angles for forward kinematics; lengths:{len(lengths)}, angles:{len(angles)}")
        return
    
    x = 0
    for i in range(0,len(lengths)):
        x += lengths[i] * math.cos(sum(angles[0:(i+1)]))

    y = 0
    for i in range(0,len(lengths)):
        y += lengths[i] * math.sin(sum(angles[0:(i+1)]))

    return (x,y)

def main():

    #TODO get the current servo angles 
    SC.goto(SERVO_BASE, 0, speed=512, degrees=True)
    SC.goto(SERVO_ELBOW, 0, speed=512, degrees=True)

    angle_base  = SC.get_present_position(SERVO_BASE, degrees=True)
    angle_elbow = SC.get_present_position(SERVO_ELBOW, degrees=True)

    camera_position = forward_kinematics([L_HUMERUS, L_CAM], [0,0])

    print(angle_base)
    print(angle_elbow)
    
    gpio.cleanup()

if __name__ == "__main__":
    main()