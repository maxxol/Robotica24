import sys
from pyax12.connection import Connection
import RPi.GPIO as gpio
import time

'''
picks up a stationary scissors that is manually placed underneath the gripper
'''

dyx_idGripper = 6 
dyx_idFingers = 14
dyx_idGripperHeight = 1
dyx_idElbow = 18
dyx_idBase = 2

rotateSpeed = 200 #half of max speed
fingerSpeed = 200
degreesBool = True #servos in degree mode

#store angles provided by the calculator
gripperAngle = float(sys.argv[1])
elbowAngle = sys.argv[2]
baseAngle = sys.argv[3]
gripperHeightRaisedAngle = -120
gripperHeightLoweredAngle = 150
fingerCloseAngle = -140
fingerOpenAngle = -20

gripperAngle = round(gripperAngle)

#gripper rotate
sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

#ALL JOINT MODE 
sc.set_cw_angle_limit(dyx_idGripper, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idGripper, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idFingers, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idFingers, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idBase, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idBase, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idGripperHeight, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idGripperHeight, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idElbow, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idElbow, 150, degrees=True)
time.sleep(2)



#RESET ALL MOTORS
sc.goto(dyx_idGripperHeight, 0, speed=fingerSpeed, degrees=degreesBool)
sc.goto(dyx_idGripper, 0, speed=(rotateSpeed), degrees=degreesBool)
sc.goto(dyx_idFingers, fingerOpenAngle, speed=fingerSpeed, degrees=degreesBool)
sc.goto(dyx_idElbow, 0, speed=rotateSpeed, degrees=degreesBool)
sc.goto(dyx_idBase, 0, speed=rotateSpeed, degrees=degreesBool)
time.sleep(10)

#pick up the kilogram cylinder
sc.goto(dyx_idElbow, 150, speed=rotateSpeed, degrees=degreesBool)
sc.goto(dyx_idBase, 150, speed=rotateSpeed, degrees=degreesBool)
time.sleep(10)

sc.goto(dyx_idElbow, -150, speed=rotateSpeed, degrees=degreesBool)
sc.goto(dyx_idBase, -150, speed=rotateSpeed, degrees=degreesBool)
time.sleep(10)

sc.goto(dyx_idElbow, 0, speed=rotateSpeed, degrees=degreesBool)
sc.goto(dyx_idBase, 0, speed=rotateSpeed, degrees=degreesBool)
time.sleep(10)




