from pyax12.connection import Connection
from time import sleep
from enum import Enum

class ServoMode(Enum):
    JOINT_MODE = 1
    WHEEL_MODE = 2

class Direction(Enum):
    CLOCKWISE = 1
    COUNTER_CLOCKWISE= 2

class Servo():
    def __init__(self, id, connection, mode=ServoMode.JOINT_MODE):
        self.id = id
        self.connection = connection

        # # Initialize servo in joint mode
        # self.change_mode(mode=mode)

    """"
        turn the servo in Joint Mode

        param angle: integer in range [-150, 150]
        param speed: float in range [0, 1]; determines the speed of servo as a percentage (0 => 0%, 1 => 100%)
    """
    def turn_degrees(self, angle, speed=0.3):
        max_servo_speed = 1023
        desired_speed = int( speed * max_servo_speed )
        self.connection.goto(self.id, position=angle, speed=512)

    """
        turn the servo in Wheel Mode

        param speed: float in range [0, 1]; determines the speed of servo as a percentage (0 => 0%, 1 => 100%)
        param cw: boolean; True for clockwise rotation; False for counter-clockwise
    """
    def turn_wheel(self, speed=0.3, direction=Direction.COUNTER_CLOCKWISE):
        if direction == Direction.COUNTER_CLOCKWISE:
            ccw_total_speed = 1023 - 0
            desired_speed   = int(speed * ccw_total_speed)
        elif direction == Direction.CLOCKWISE:
            cw_total_speed = 2047 - 1024
            desired_speed  = 1023 + int(speed * cw_total_speed)
        else:
            print(f"Invalid parameters: (speed:{speed}, direction:{direction})")
            
        self.connection.set_speed(self.id, desired_speed)

    """
        Stops the wheel mode rotation 
    """
    def stop_wheel(self):
        self.connection.set_speed(self.id, 0) 


    def get_mode(self, debug=False):
        cw_angle_limit  = self.connection.get_cw_angle_limit(self.id)
        ccw_angle_limit = self.connection.get_ccw_angle_limit(self.id)

        if debug:
            print(f"servo_id: {self.id}, cw_limit: {cw_angle_limit}")
            print(f"servo_id: {self.id}, ccw_limit: {ccw_angle_limit}")

        if (cw_angle_limit == ccw_angle_limit) and cw_angle_limit == 0:
            return ServoMode.WHEEL_MODE
        elif (cw_angle_limit == 0) and (ccw_angle_limit == 1023):
            return ServoMode.JOINT_MODE 
        else:
            raise ModeError('Servo settings are incorrect')

    """
        To toggle between wheel (continuous turn) and joint (instructed turn) modes the ccw and cw angle limits need to be set 
        in the control table of the servo

        param mode: enum ServoMode; indicates which mode to switch to
    """
    def change_mode(self, mode, debug=False):
        if debug:
            print(f"change mode: {mode}")
        if mode == ServoMode.WHEEL_MODE:
            if debug:
                print("setting to wheel mode")
            self.connection.set_cw_angle_limit(self.id, 0, degrees=False)
            sleep(1)        #include sleep statements to prevent timing issues

            self.connection.set_ccw_angle_limit(self.id, 0, degrees=False)
            sleep(1)        #include sleep statements to prevent timing issues
        elif mode == ServoMode.JOINT_MODE:
            if debug:           
                print("setting to joint mode")
            self.connection.set_cw_angle_limit(self.id, -150, degrees=True)
            sleep(1)        #include sleep statements to prevent timing issues
            
            self.connection.set_ccw_angle_limit(self.id, 150, degrees=True)
            sleep(1)

    