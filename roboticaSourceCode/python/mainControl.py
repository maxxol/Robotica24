from bluetooth import BluetoothHandler
from pyax12.connection import Connection
import serial
import datetime
from servo import Servo, ServoMode, Direction

rfcomm_port = "/dev/rfcomm0"
connect_script = "../shell/connect_rfcomm.sh"
disconnect_script = "../shell/disconnect_rfcomm.sh"

# Connection to servo's
SC = Connection(port="/dev/serial0",baudrate=1000000, rpi_gpio=True)

# Servo ID's
SERVO_GRIP        = Servo(id=14, connection=SC)
SERVO_ROTATE      = Servo(id=6,  connection=SC) 
SERVO_VERTICAL    = Servo(id=1,  connection=SC)
SERVO_ELBOW       = Servo(id=18, connection=SC)
SERVO_SHOULDER    = Servo(id=2,  connection=SC)
servos = [SERVO_GRIP, SERVO_ROTATE, SERVO_VERTICAL, SERVO_ELBOW, SERVO_SHOULDER]

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
                SERVO_ROTATE.turn_wheel(direction=Direction.COUNTER_CLOCKWISE)
            elif gr_cw:
                SERVO_ROTATE.turn_wheel(direction=Direction.CLOCKWISE)            

            if gr_close:
                SERVO_GRIP.turn_wheel(direction=Direction.CLOCKWISE)
            elif gr_open:
                SERVO_GRIP.turn_wheel(direction=Direction.COUNTER_CLOCKWISE)

            if joystick_z > 50:
                SERVO_VERTICAL.turn_wheel(speed=0.6, direction=Direction.CLOCKWISE)
            elif joystick_z < -50:
                SERVO_VERTICAL.turn_wheel(speed=0.5, direction=Direction.COUNTER_CLOCKWISE)
            elif -50 < joystick_z < 50:
                SERVO_VERTICAL.stop_wheel()

            if joystick_x > 50:
                SERVO_ELBOW.turn_wheel(direction=Direction.CLOCKWISE)
            elif joystick_x < -50:
                SERVO_ELBOW.turn_wheel(direction=Direction.COUNTER_CLOCKWISE)
            elif -50 < joystick_x < 50:
                SERVO_ELBOW.stop_wheel()

            if joystick_y > 50:
                SERVO_SHOULDER.turn_wheel(speed=0.5, direction=Direction.CLOCKWISE)
            elif joystick_y < -50:
                SERVO_SHOULDER.turn_wheel(speed=0.6, direction=Direction.COUNTER_CLOCKWISE)
            elif -50 < joystick_y < 50:
                SERVO_SHOULDER.stop_wheel()

            if gr_ccw == gr_cw:
                SERVO_ROTATE.stop_wheel()
                
            if gr_open == gr_close:
                SERVO_GRIP.stop_wheel()
                
        case 2:
            # print("Joint mode grippers")
            # for s in servos:
            #     set_joint_mode(s)
            print("Mollen meppen")
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
    for servo in servos:
        current_mode = servo.get_mode(debug=False)
        if current_mode == ServoMode.JOINT_MODE:
            servo.change_mode(mode=ServoMode.WHEEL_MODE)

    # # BluetoothScanner to find Bluetooth connection TODO
    # connected = False
    # # while (not connected):

    # Make connection to bluetooth
    bt = BluetoothHandler(rfcomm_port, connect_script, disconnect_script)
    try:
        while True:
            data = bt.read_data()
            print(f"current_data: {data}")
            if len(data) > 0:
                process_data(data)
            elif len(data) <= 0:
                pass #TODO STOP ALL SERVO MOVEMENT
    except KeyboardInterrupt:
        print("Program interrupted by user")
        #Close connection 
        bt.close()
        bt.disconnect()

            


if __name__ == "__main__":
    main()