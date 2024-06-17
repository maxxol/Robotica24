from bluetooth import BluetoothHandler
from pyax12.connection import Connection
import serial
import datetime

rfcomm_port = "/dev/rfcomm0"
connect_script = "../shell/connect_rfcomm.sh"
disconnect_script = "../shell/disconnect_rfcomm.sh"

# Connection to servo's
SC = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

# Servo ID's
SID_SERVO_GRIP        = 14
SID_SERVO_ROTATE      = 6 
SID_SERVO_VERTICAL    = 1
SID_SERVO_ELBOW       = 18
SID_SERVO_SHOULDER    = 2
servos = [SID_SERVO_GRIP, SID_SERVO_ROTATE, SID_SERVO_VERTICAL, SID_SERVO_ELBOW, SID_SERVO_SHOULDER]

# Other constants
gripperCloseAngle = -140
gripperOpenAngle = -20
gripSpeed = 200


def set_wheel_mode(servo_id):
    SC.set_cw_angle_limit(servo_id, 0, degrees=False)
    SC.set_ccw_angle_limit(servo_id, 0, degrees=False)

def set_joint_mode(servo_id):
    SC.set_cw_angle_limit(servo_id, -150, degrees=True)
    SC.set_ccw_angle_limit(servo_id, 150, degrees=True) 

def turn_cw():
    SC.set_speed(SID_SERVO_ROTATE, 1224)

def turn_ccw():
    SC.set_speed(SID_SERVO_ROTATE, 200)

def open_gripper():
    SC.set_speed(SID_SERVO_GRIP, 600)

def close_gripper():
    SC.set_speed(SID_SERVO_GRIP, 1500)

def move_up():
    SC.set_speed(SID_SERVO_VERTICAL, 1624)

def move_down():
    SC.set_speed(SID_SERVO_VERTICAL, 600)

def elbow_ccw():
    SC.set_speed(SID_SERVO_ELBOW, 200)

def elbow_cw():
    SC.set_speed(SID_SERVO_ELBOW, 1224)

def shoulder_ccw():
    SC.set_speed(SID_SERVO_SHOULDER, 400)

def shoulder_cw():
    SC.set_speed(SID_SERVO_SHOULDER, 1424)

def process_data(data):
    stand       = data[0]
    gr_open     = data[1]
    gr_close    = data[2]
    gr_ccw      = data[3]
    gr_cw       = data[4]
    joystick_x  = data[5]
    joystick_y  = data[6]
    joystick_z  = data[7]

    match stand:
        case 1:
            if gr_ccw:
                print(f"Turn ccw")
                turn_ccw()
                return
            elif gr_cw:
                print(f"Turn cw")
                turn_cw()
                return
                
            if gr_close:
                print(f"Close")
                close_gripper()
                return
            elif gr_open:
                print(f"Open")
                open_gripper()
                return

            if joystick_z > 50:
                move_up()
                return
            elif joystick_z < -50:
                move_down()
                return
            elif -50 < joystick_z < 50:
                SC.set_speed(SID_SERVO_VERTICAL, 0)

            if joystick_x > 50:
                elbow_cw()
                return
            elif joystick_x < -50:
                elbow_ccw()
                return
            elif -50 < joystick_x < 50:
                SC.set_speed(SID_SERVO_ELBOW, 0)

            if joystick_y > 50:
                shoulder_cw()
                return
            elif joystick_y < -50:
                shoulder_ccw()
                return
            elif -50 < joystick_y < 50:
                SC.set_speed(SID_SERVO_SHOULDER, 0)

            if gr_ccw == gr_cw:  #Both buttons are pressed or not pressed (xnor)
                print("both rotations")
                SC.set_speed(SID_SERVO_ROTATE, 0)
                
            if gr_close == gr_open:
                print("both open/close")
                SC.set_speed(SID_SERVO_GRIP, 0)
                
        case 2:
            print("Joint mode grippers")
            for s in servos:
                set_joint_mode(s)
        case 3:
            print("Groen")
        case 4:
            print("Rood")
        case 5:
            print("Blauw")
        case 6:
            print("Magenta")
        case 7:
            print("Silver")

def main():

    #setup servos
    set_wheel_mode(SID_SERVO_ROTATE)
    set_wheel_mode(SID_SERVO_GRIP)
    set_wheel_mode(SID_SERVO_VERTICAL)
    set_wheel_mode(SID_SERVO_ELBOW)
    set_wheel_mode(SID_SERVO_SHOULDER)

    # # BluetoothScanner to find Bluetooth connection TODO
    # connected = False
    # # while (not connected):

    # Make connection to bluetooth
    bt = BluetoothHandler(rfcomm_port, connect_script, disconnect_script)
    try:
        while True:
            data = bt.read_data()
            print(data)
            process_data(data)
    except KeyboardInterrupt:
        print("Program interrupted by user")
        #Close connection 
        bt.close()
        bt.disconnect()

            


if __name__ == "__main__":
    main()