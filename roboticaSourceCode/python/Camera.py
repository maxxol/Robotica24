import cv2


class Camera:
    def __init__(self, fps, resolution_x, resolution_y):
        self.fps = fps
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y

    def zet_camera_aan(self):
        # Hierin wordt de camera aangezet
        #print('connecting')
        camera = cv2.VideoCapture(0)
        #print("done")
        # camera.set(cv2.CAP_PROP_FPS, self.fps)

        current_fps = camera.get(cv2.CAP_PROP_FPS)
        #print("Current FPS:", current_fps)
        return camera

    def zet_camera_uit(self, cap):
        # Hierin wordt de camera uitgezet.

        cap.release()
        cv2.destroyAllWindows()
        pass

