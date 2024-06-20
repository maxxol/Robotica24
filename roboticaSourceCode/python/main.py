from Camera import Camera
from KleurenStand import KleurenStand
from TargetStand import TargetStand
from DataSender import DataSender
import cv2
from bluetooth import BluetoothHandler
from Silver import Silver

#from bluetooth import connect_rfcomm, read_signed_integers
# import serial

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

stand = 3


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
    si = Silver()
    ts = TargetStand()

    match stand:
        case 1:
            print('robot staat in manual stand')
            return
        case 2:
            _, frame = cap.read()
            target = ts.vind_target(frame)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if target:
                # ds.verstuur_target_coordinaten(target)
                print(target)
                return target
            else:
                return None
        case 3:
            _, frame = cap.read()
            object_data = si.detect(frame, focus_object)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
            #     ds.verstuur_object_coordinaten(object_data)
                print(object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1])
                return object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1]
            else: 
                return None
        case 4:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'rood', focus_object)


            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
            #     ds.verstuur_object_coordinaten(object_data)
                print(object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1])
                return object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1]
            else: 
                return None
        case 5:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'groen', focus_object)
            
            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
            #     ds.verstuur_object_coordinaten(object_data)
                print(object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1])
                return object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1]
            else: 
                return None
        case 6:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'blauw', focus_object)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
            #     ds.verstuur_object_coordinaten(object_data)
                print(object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1])
                return object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1]
            else: 
                return None
        case 7:
            _, frame = cap.read()
            object_data = ks.detect(frame, 'magenta', focus_object)


            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg', frame)
            if object_data:
            #     ds.verstuur_object_coordinaten(object_data)
                print(object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1])
                return object_data[0], object_data[1], object_data[3][0], object_data[3][1], object_data[4][0], object_data[4][1]
            else: 
                return None
    return print('Geen stand geselecteerd')


# def verander_stand(input_controller):
#     """
#     In deze functie wordt de stand variabele aangepast
#     door de standenschakelaar van de controller

#     Parameters:
#         input_controller (int): de huidige stand op de controller.
#     """
#     stand = input_controller
#     return


if __name__ == '__main__':
    main('PyCharm', None)
