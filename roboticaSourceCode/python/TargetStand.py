import math
import cv2
import numpy as np
from Objecten import Objecten


# deze class kan wellicht overerven van de klasse kleurherkenning, omdat de target op kleur wordt herkend
class TargetStand:
    # inladen afbeelding van target voor testen code
    def __init__(self):
        # min & max hsv waarden voor geel
        self.geel_onderste = np.array([20, 100, 100], np.uint8)
        self.geel_bovenste = np.array([30, 255, 255], np.uint8)

    def vind_target(self, frame):

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # gele mask kan later ook uit kleurherkenning gehaald worden
        geel_mask = cv2.inRange(hsv_frame, self.geel_onderste, self.geel_bovenste)
        geel_mask = cv2.morphologyEx(geel_mask, cv2.MORPH_OPEN, (5, 5))

        # vind buitenste contouren van gele mask (external), slaat deze op in lijst
        contours = cv2.findContours(geel_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for c in contours:

            area = cv2.contourArea(c)

            if area < 300:
                continue

            # berekent omtrek contour c & slaat punten op in lijst
            hull = cv2.convexHull(c)
            # tekent alle contouren uit lijst hull op de image in het oranje, met dikte 2
            cv2.drawContours(frame, [hull], -1, (0, 165, 255), 2)

            # berekent eigenschappen van een vorm
            m = cv2.moments(c)

            try:
                # x coördinaat berekenen centroid (centroid)
                # m10 & m00 worden berekend door cv2.moments. m10 som van x-coördinaten alle pixels, m00 is totaal aantal pixels contour
                cx = int(m['m10'] / m['m00'])
            except ZeroDivisionError:
                # zet cx op 0 print het resultaat van de cx berekening als er wordt gedeeld door 0
                cx = 0
                print("Result of {} / {}: {}".format(m['m10'], m['m00'], cx))

            try:
                # y coördinaat berekenen centroid (centroid)
                # m01 & m00 worden berekend door cv2.moments. m01 som van y-coördinaten alle pixels, m00 is totaal aantal pixels contour
                cy = int(m['m01'] / m['m00'])
            except ZeroDivisionError:
                # zet cy op 0 en print het resultaat van cy berekening bij delen door 0
                cy = 0
                print("Result of {} / {}: {}".format(m['m01'], m['m00'], cy))

            # tekent stip in het midden van de cirkel met coördinaten cx,cy
            frame = cv2.circle(frame, (cx, cy), 5, (0, 165, 255), -1)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/target.jpg', frame)

            return cx, cy


