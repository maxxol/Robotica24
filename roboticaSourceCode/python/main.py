from Camera import Camera
from KleurenStand import KleurenStand
from TargetStand import TargetStand
from DataSender import DataSender
import cv2

stand = 5


def main():
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
            #print('robot staat in manual stand')
            return
        case 2:
            # _, frame = cap.read()
            frame = r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg'
            target = ts.vind_target(frame)
            if target:
                ds.verstuur_target_coordinaten(target)
            return
        case 3:
            # _, frame = cap.read()
            # frame = ks.detect(frame)
            object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'grijs')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 4:
            # _, frame = cap.read()
            # frame = ks.detect(frame)
            object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'rood')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 5:
            _, frame = cap.read()
            cv2.imwrite("/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/schaarRecht.jpg",frame)
            object_data = ks.detect(frame, 'groen')

            # object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240523_134228.png', 'groen')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 6:
            # _, frame = cap.read()
            # frame = ks.detect(frame)
            object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'blauw')
            if object_data:
                ds.verstuur_object_coordinaten(object_data)
            return
        case 7:
            # _, frame = cap.read()
            # frame = ks.detect(frame)
            object_data = ks.detect(r'C:\Users\thoma\PycharmProjects\Computer_Vision\20240604_135023.jpg', 'magenta')
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
