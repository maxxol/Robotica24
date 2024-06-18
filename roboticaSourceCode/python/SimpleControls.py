from pyax12.connection import Connection



# TODO figure out if this is necessary
class SimpleControl:
    def __init__(self):
        print("Basic controls active")
        self.connection = Connection(port="/dev/serial0", baudrate=1_000_000, rpi_gpio=True)

    # """
    #     turn clockwise function
    # """
    # def turn_cw(self, servo_id, speed=0.5):
    #     max_speed = 2047 - 1024
    #     desired_speed = speed * max_speed


    # def turn_ccw(self):
