import RPi.GPIO as gpio


gpio.setup(18, gpio.OUT)

gpio.output(18, gpio.LOW)


gpio.cleanup()

