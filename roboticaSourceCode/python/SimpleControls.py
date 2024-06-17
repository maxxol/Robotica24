from pyax12.connection import Connection


class SimpleControl:
    def __init__():
        print("Basic controls active")
        self.connection = Connection(port="/dev/serial0", baudrate=1_000_000, rpi_gpio=True)