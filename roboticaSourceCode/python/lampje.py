import RPi.GPIO as gpio

#Pin definitions. Tells to which GPIO pin the letter is connected
A = 17
B = 27
C = 22
D = 10 

def setup():
    # set board mode
    gpio.setmode(gpio.BCM)

    #gpio.setup() # set the pins to output mode
    gpio.setup(A, gpio.OUT)
    gpio.setup(B, gpio.OUT)
    gpio.setup(C, gpio.OUT)
    gpio.setup(D, gpio.OUT) 

#stop sending binary code and cleanup the gpio
def shutdown():
    gpio.cleanup()

def sendBinaryCode(a, b, c, d):

    gpio.output(A, a)
    gpio.output(B, b)
    gpio.output(C, c)
    gpio.output(D, d) 
    
#for the display anode is used, which means that all bits that should be high are 0, and all low are 1
#send number one to display
def one():
    sendBinaryCode(1, 1, 1, 0)

#send number two to display
def two():
    sendBinaryCode(1, 1, 0, 1)

#send number three to display
def three():
    sendBinaryCode(1, 1, 0, 0)

#send number four to display
def four():
    sendBinaryCode(1, 0, 1, 1)

#send number five to display
def five():
    sendBinaryCode(1, 1, 0, 0)

#send number six to display
def six():
    sendBinaryCode(1, 0, 0, 1)

#send number seven to display
def seven():
    sendBinaryCode(1, 0, 0, 0)

#turn all lights off / set all pins to low
def reset():
    sendBinaryCode(1, 1, 1, 1)


#main function
def main():

    #call setup mode to set pins and board mode
    setup()

    print("Hello World")
    one()

    shutdown()


if __name__ == "__main__":
    main()
