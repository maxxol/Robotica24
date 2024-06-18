from Camera import Camera
from KleurenStand import KleurenStand
from TargetStand import TargetStand
from DataSender import DataSender
import cv2
from bluetooth import BluetoothHandler

#from bluetooth import connect_rfcomm, read_signed_integers
import serial

# rfcomm_port = "/dev/rfcomm0"
# connect_script = "../shell/connect_rfcomm.sh"
# disconnect_script = "../shell/disconnect_rfcomm.sh"

# bt = BluetoothHandler(rfcomm_port, connect_script, disconnect_script)
# try:
#     while True:
#         data = bt.read_data()
#         print(data)
#         process_data(data)
# except KeyboardInterrupt:
#     print("Program interrupted by user")
#     #Close connection 
#     bt.close()
#     bt.disconnect()

stand = 5


def main(name, focus_object):
    """
    De main functie. De robot heeft 7 verschillende standen waarin het kan schakelen;
    Manual, Target en elk van de kleuren een eigen stand.

    Parameters:
        name (str): 'PyCharm'
    """
    aan = True
    camera = Camera(10.0, 480, 360)
    cap = camera.zet_camera_aan()
    ds = DataSender()
    ks = KleurenStand()
    ts = TargetStand()

    match stand:
        case 1:
            print('robot staat in manual stand')
            return
        case 2:
            _, frame = cap.read()
            target = ts.detect(frame, 'target')

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if target:
                ds.verstuur_target_coordinaten(target)
            return
        case 3:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'grijs', focus_object)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 4:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'rood', focus_object)


            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 5:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'groen', focus_object)
            
            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 6:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'blauw', focus_object)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 7:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'magenta', focus_object)


            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
    return print('Geen stand geselecteerd')


def verander_stand(input_controller):
    """
    In deze functie wordt de stand variabele aangepast
    door de standenschakelaar van de controller

    Parameters:
        input_controller (int): de huidige stand op de controller.
    """
    stand = input_controller
    return


if __name__ == '__main__':
    main('PyCharm', None)
