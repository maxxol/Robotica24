import sys
from pyax12.connection import Connection
import RPi.GPIO as gpio
import time
#from ~/py_robotica/demo.py import change_mode,wheel_turn
print("external python rotateServos has run with parameter", sys.argv[1],sys.argv[2],sys.argv[3])

dyx_idGripper = 6 
dyx_idFingers = 14
dyx_idGripperHeight = 1
dyx_idElbow = 18
dyx_idBase = 2

rotateSpeed = 100 #half of max speed
fingerSpeed = 200
degreesBool = True #servos in degree mode

#store angles provided by the calculator
gripperAngle = float(sys.argv[1])
elbowAngle = sys.argv[2]
baseAngle = sys.argv[3]
gripperHeightRaisedAngle = -140
gripperHeightLoweredAngle = 150
fingerCloseAngle = -100
fingerOpenAngle = -20

gripperAngle = round(gripperAngle)





#gripper rotate
sc = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

# #SC.write_data(servo_idx, pk.CW_ANGLE_LIMIT, 0)
# sc.set_cw_angle_limit(dyx_idGripper, -150, degrees=True)
# time.sleep(1)
# #SC.write_data(servo_idx, pk.CCW_ANGLE_LIMIT, 0)
# sc.set_ccw_angle_limit(dyx_idGripper, 150, degrees=True)
# time.sleep(1)
# sc.goto(dyx_idElbow, 0, speed=rotateSpeed, degrees=degreesBool)
# time.sleep(10)
# sc.goto(dyx_idElbow, 150, speed=rotateSpeed, degrees=degreesBool)
# time.sleep(10)
# sc.goto(dyx_idElbow, -150, speed=rotateSpeed, degrees=degreesBool)
# time.sleep(10)
#sc.pretty_print_control_table(dyx_idFingers)


# sc.goto(dyx_idGripperHeight, gripperHeightLoweredAngle, speed=rotateSpeed, degrees=degreesBool)
# sc.goto(dyx_idGripper, gripperAngle, speed=rotateSpeed, degrees=degreesBool)
# time.sleep(2)

# sc.goto(dyx_idFingers, fingerCloseAngle, speed=fingerSpeed, degrees=degreesBool)
# time.sleep(2)

# sc.goto(dyx_idGripperHeight, gripperHeightRaisedAngle , speed=rotateSpeed, degrees=degreesBool)
# sc.goto(dyx_idGripper, 0, speed=rotateSpeed, degrees=degreesBool)
# time.sleep(2)

# sc.goto(dyx_idFingers, fingerOpenAngle, speed=fingerSpeed, degrees=degreesBool)
# time.sleep(2)



#ALL JOINT MODE 
sc.set_cw_angle_limit(dyx_idGripper, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idGripper, 150, degrees=True)
#time.sleep(1)
#SC.write_data(servo_idx, pk.CCW_ANGLE_LIMIT, 0)

#time.sleep(1)

sc.set_cw_angle_limit(dyx_idFingers, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idFingers, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idBase, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idBase, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idGripperHeight, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idGripperHeight, 150, degrees=True)

sc.set_cw_angle_limit(dyx_idElbow, -150, degrees=True)
sc.set_ccw_angle_limit(dyx_idElbow, 150, degrees=True)
time.sleep(2)
#SC.write_data(servo_idx, pk.CCW_ANGLE_LIMIT, 0)

#time.sleep(1)



#RESET ALL MOTORS
sc.goto(dyx_idGripperHeight, 0, speed=fingerSpeed, degrees=degreesBool)
sc.goto(dyx_idGripper, 0, speed=(rotateSpeed), degrees=degreesBool)
sc.goto(dyx_idFingers, fingerOpenAngle, speed=fingerSpeed, degrees=degreesBool)
sc.goto(dyx_idElbow, 0, speed=rotateSpeed, degrees=degreesBool)
sc.goto(dyx_idBase, 0, speed=rotateSpeed, degrees=degreesBool)
time.sleep(200)


'''
#elbow rotate
sc.goto(dyx_idElbow, elbowAngle, speed=rotateSpeed, degrees=degreesBool)

#base rotate
sc.goto(dyx_idBase, baseAngle, speed=rotateSpeed, degrees=degreesBool)
'''
#time.sleep(1)
# sc.goto(dyx_idGripper, 0, speed=rotateSpeed, degrees=degreesBool)
# time.sleep(1)
