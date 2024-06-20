from KleurenStand import KleurenStand
import cv2
import numpy as np


class Silver(KleurenStand):
    def __init__(self):
        super().__init__()

    def detect(self, frame, focus_object):

        # Als je de objectherkenning wilt testen op een image path, dan kan je dit hieronder gebruiken. Anders #.
        # frame = cv2.imread(frame)
        # scale_factor = 0.8
        # frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if focus_object:
            self.objecten.focus_object = focus_object

        self.frame = frame

        self.detect_silver(frame)

        if len(self.objecten.nieuw) == 0 or None:
            self.objecten.verwijder_object()
        else:
            focus_object = self.objecten.update_positie()
            self.teken_contouren(frame)
            return focus_object
        return

    def detect_silver(self, frame):
        grijs_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grijs_frame, 100, 200)
        edges = self.fill_edges(edges)
        # edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, self.kernel)

        # cv2.imwrite(r'C:\Users\thoma\PycharmProjects\Computer_Vision\img\edges.png', edges)
        #
        # cv2.imshow('frame', edges)
        # cv2.waitKey(0)

        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for contour in contours:
            area = cv2.contourArea(contour)
            if 1000 < area < 25000:
                if self.is_silver(hsv, contour):
                    rect = cv2.minAreaRect(contour)
                    type_object = self.object_herkenning(rect, contour, grijs_frame)
                    cx, cy = self.centroid(contour)
                    vx, vy, x, y = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)

                    if type_object is not None and type_object != "idk":
                        if self.objecten.nieuw != {}:
                            last_item = next(reversed(self.objecten.nieuw))
                            new_item = int(last_item) + 1
                            self.objecten.nieuw.update({new_item: (type_object, 'silver', rect, (cx, cy), (vx, vy, x, y))})
                        else:
                            self.objecten.nieuw.update({1: (type_object, 'silver', rect, (cx, cy), (vx, vy, x, y))})

    def is_silver(self, hsv, contour):
        masker_rood1 = cv2.inRange(hsv, self.rood_onderste, self.rood_bovenste)
        masker_rood2 = cv2.inRange(hsv, self.rood_onderste2, self.rood_bovenste2)
        masker_rood = cv2.bitwise_or(masker_rood1, masker_rood2)

        masker_groen = cv2.inRange(hsv, self.groen_onderste, self.groen_bovenste)
        masker_blauw = cv2.inRange(hsv, self.blauw_onderste, self.blauw_bovenste)
        masker_magenta = cv2.inRange(hsv, self.magenta_onderste, self.magenta_bovenste)

        x, y, w, h = cv2.boundingRect(contour)
        roi = hsv[y:y + h, x:x + w]

        masker_rood_roi = masker_rood[y:y + h, x:x + w]
        masker_groen_roi = masker_groen[y:y + h, x:x + w]
        masker_blauw_roi = masker_blauw[y:y + h, x:x + w]
        masker_magenta_roi = masker_magenta[y:y + h, x:x + w]

        rood_detected = cv2.countNonZero(masker_rood_roi) > 100
        groen_detected = cv2.countNonZero(masker_groen_roi) > 100
        blauw_detected = cv2.countNonZero(masker_blauw_roi) > 100
        magenta_detected = cv2.countNonZero(masker_magenta_roi) > 100

        return not (rood_detected or groen_detected or blauw_detected or magenta_detected)

    def fill_edges(self, edges):
        
        kernel = np.ones((5, 5), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)

        h, w = dilated_edges.shape[:2]
        masker = np.zeros((h + 2, w + 2), np.uint8)

        flood_filled = dilated_edges.copy()
        cv2.floodFill(flood_filled, masker, (0, 0), 255)

        flood_filled_inv = cv2.bitwise_not(flood_filled)

        filled_edges = dilated_edges | flood_filled_inv

        return filled_edges