import serial 
import struct
import subprocess
from time import sleep
import os

# Manual connect with bluetooth 
#1. hcitool scan -> get MAC address
#2. sudo rfcomm connect hci0 <MAC address>
#3. Open new terminal
#4. Navigate to ~/py_robotica and execute script bluetooth_test
#5. Serial communication between raspberry pi and esp32 becomes possible

class BluetoothHandler:
    def __init__(self, port=None, connect=None, disconnect=None):
        if port is None:
            raise Exception("Device port is not defined")
        elif connect is None:
            raise Exception("Connect script is not defined")
        elif disconnect is None:
            raise Exception("Disconnect script is not defined")

        self.serial = None
        self.port = port
        self.connection = connect
        self.disconnection = disconnect

        self.connect()
        self.open()

    def connect(self):
        try:
            print("Connecting to ESP32...")
            sub_proc = subprocess.Popen(self.connection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            timeout = 10  # seconds
            for _ in range(timeout):
                if os.path.exists("/dev/rfcomm0"):
                    print("rfcomm device created successfully")            
                    return sub_proc
                sleep(1)

            # If we reach here, the device was not created
            sub_proc.terminate()
            print("Failed to create rfcomm device within timeout period")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")

    def open(self):
        try:
            print("Opening serial port...")
            self.serial = serial.Serial(self.port, baudrate=9600, timeout=1)
            print("Serial port opened successfully")
            #sleep(5) #before data is sent, there is a delay
        except serial.SerialException as se:
            print(f"Serial Exception: {str(se)}")
        except KeyboardInterrupt:
            print("Program interrupted by user")

    def read_data(self, debug=False):
        controller_data = () #controller data gets stored in this variable as a tuple
        
        if debug:
            print(f"serial waiting: {self.serial.in_waiting}")

        # Buffer has not received any data yet if serial.in_waiting == 0
        while self.serial.in_waiting == 0:
            pass
        
        # Read 9 bytes of datas
        data = self.serial.read(9)
        #print(f"Raw Data: {data}")
        # if starting byte found, unpack data
        if data[0] == 0xFF:
            data = data[1:]   # Remove starting byte
            controller_data = struct.unpack('8b', data)
            print(f"Collected data: {controller_data}")
        else:
            print("Flushing input buffer")
            self.serial.flush() #flush the buffer
            print(f"buffer size: {self.serial.in_waiting}")
                
        return controller_data

    def close(self):
        self.serial.close()

    def disconnect(self):
        try: 
            print("Disconnecting from ESP32...")
            sub_proc = subprocess.Popen(self.disconnection, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            print(f"Exception: {str(e)}")
        # finally:
        #     print("Disconnected from ESP32")
        #     sub_proc.terminate()
        
def main():    
    connect_script = "../shell/connect_rfcomm.sh"
    disconnect_script = "../shell/disconnect_rfcomm.sh"
    rfcomm_port = "/dev/rfcomm0"

    bt = BluetoothHandler(rfcomm_port, connect_script, disconnect_script)
    try:
        while True:
            data = bt.read_data()
            #print(data)
    except KeyboardInterrupt:
        print("Program interrupted by user")
        bt.close()
        bt.disconnect()

if __name__ == "__main__":
    main()
    
    

