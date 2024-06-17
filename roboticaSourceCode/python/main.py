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


def main():
    
    aan = True
    camera_index = 0
    cam = cv2.VideoCapture(camera_index)
    ds = DataSender()
    ks = KleurenStand()
    ts = TargetStand()

    stand = 4

    match stand:
        case 1:

            return
        case 2:
            # _, frame = cap.read()
            frame = r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg'
            target = ts.vind_target(frame)
            if target:
                ds.verstuur_target_coordinaten(target)
            return
        case 3:
            _, frame = cam.read()
            frame = ks.detect(frame, "grijs")
            #cv2.imwrite("/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarGrijs.jpg", frame)
            #object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'grijs')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 4:
            _, frame = cam.read()
            frame = ks.detect(frame, "rood")
            #cv2.imwrite("/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRood.jpg", frame)
            #object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'rood')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 5:
            _, frame = cam.read()
            object_data = ks.detect(frame, 'groen')
            #cv2.imwrite("/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarGroen.jpg", frame)
            # object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240523_134228.png', 'groen')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 6:
            _, frame = cam.read()
            frame = ks.detect(frame, 'blauw')
            #object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'blauw')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 7:
            _, frame = cam.read()
            frame = ks.detect(frame, 'magenta')
            #object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'magenta')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
    return #print('Geen stand geselecteerd')


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
    main()

# Image paths voor het silvere blokje
# frame = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\Silverblokje\20240606_114432.jpg')
# frame = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\Silverblokje\20240606_114437.jpg')
# frame = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\Silverblokje\20240606_114441.jpg')
# frame = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\Silverblokje\20240606_114459.jpg')

# Kleuren: rood, groen, blauw, magenta, silver/grijs

# cv2.imshow("Live kleur detectie", frame)
# cv2.waitKey(0)

# _, frame = cap.read()
#
# frame_with_detection = ks.detect(frame, 'groen')
#
# ds.verstuur_object_coordinaten(frame_with_detection)
#
# cv2.imshow('Object Detection', frame_with_detection)
#
# if cv2.waitKey(1) & 0xFF == ord('q'):
#     return
