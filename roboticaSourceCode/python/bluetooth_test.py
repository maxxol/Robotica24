import serial 
import struct
import subprocess
from time import sleep
import os

connect_script = "/home/rob8/Robotica24/roboticaSourceCode/shell/connect_rfcomm.sh"
disconnect_script = "/home/rob8/Robotica24/roboticaSourceCode/shell/disconnect_rfcomm.sh"

rfcomm_port = "/dev/rfcomm0"

def connect_rfcomm():
    try:
        print("Connecting to ESP32...")
        sub_proc = subprocess.Popen(connect_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        timeout = 10  # seconds
        for _ in range(timeout):
            if os.path.exists(rfcomm_port):
                print("rfcomm device created successfully")            
                return sub_proc
            sleep(1)

        # If we reach here, the device was not created
        sub_proc.terminate()
        print("Failed to create rfcomm device within timeout period")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")

def read_signed_integers(serial):
    controller_data = () #controller data gets stored in this variable as a tuple

    if serial.in_waiting > 0: 
        data = serial.read(8) # Read packets of 8 bytes at a time
        #print(data)
        
        controller_data = struct.unpack('8b', data)
        
        # for i in range(0,len(data)):
        #     print(f"Received data test 2 {i}: {controller_data[i]}")
        # print()

    return controller_data
        

    
def main():
    connect_rfcomm()
    try:
        print("Opening serial port...")
        ser = serial.Serial(rfcomm_port, baudrate=115200, timeout=1)
        print("Serial port opened successfully")

        while True:
            controller_data = read_signed_integers(ser)
            if len(controller_data) > 0:
                print("Data received")
                print(controller_data)
    except serial.SerialException as se:
        print(f"Serial Exception: {str(se)}")
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        if ser.is_open:
            ser.close()
            print("Serial port closed")


if __name__ == "__main__":
    main()
    
    

