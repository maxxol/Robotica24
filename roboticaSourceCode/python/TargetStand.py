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

    def detect(self, frame, actie):
        # Als je de objectherkenning wilt testen op een image path, dan kan je dit hieronder gebruiken. Anders #.
        # frame = cv2.imread(frame)
        # scale_factor = 0.2
        # frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        if actie == "target":
            centroid = self.vind_target(frame)

            return centroid
        elif actie == "contour":
            type_tang, centroid = self.vind_contour(frame)

            return type_tang, centroid
        return

    def vind_target(self, frame):

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # gele mask kan later ook uit kleurherkenning gehaald worden
        geel_mask = cv2.inRange(hsv_frame, self.geel_onderste, self.geel_bovenste)

        # vind buitenste contouren van gele mask (external), slaat deze op in lijst
        contours = cv2.findContours(geel_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for c in contours:

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

    def vind_contour(self, frame):

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # gele mask kan later ook uit kleurherkenning gehaald worden
        geel_mask = cv2.inRange(hsv_frame, self.geel_onderste, self.geel_bovenste)

        # vind buitenste contouren van gele mask (external), slaat deze op in lijst
        contours = cv2.findContours(geel_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for c in contours:

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

            v_punt = self.verst_liggende_punt(c, (cx, cy), frame)
            afstand = self.euclidean_distance(v_punt, (cx, cy))
            print(afstand)

            if 85 <= afstand <= 100:
                print("rechte tang" + " " + str(afstand))
                type_tang = 'recht'
                pass
            if 0 <= afstand <= 30:
                print("kromme tang" + " " + str(afstand))
                type_tang = 'krom'
                pass
            else:
                print("idk" + " " + str(afstand))
                type_tang = 'idk'
                pass

            # tekent stip in het midden van de cirkel met coördinaten cx,cy
            frame = cv2.circle(frame, (cx, cy), 5, (0, 165, 255), -1)

            cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/contour.jpg', frame)

            return type_tang, (cx, cy)

    # def verst_liggende_punt(self, contour, centroid, frame):
    #     """
    #     Er wordt hier het verste punt van de tang gevonden, wat nodig is voor het object herkenning.
    #     Er wordt berekend welke van de 4 verste punten van het object het meest van de centroid ligt.
    #     Dit punt is altijd de punt van de tang.
    #
    #     Parameters:
    #         contour: Een contour.
    #     """
    #     # De vier variabelen hieronder zijn de verste punten gevonden in de contour van de tang.
    #     links = tuple(contour[contour[:, :, 0].argmin()][0])
    #     rechts = tuple(contour[contour[:, :, 0].argmax()][0])
    #     top = tuple(contour[contour[:, :, 1].argmin()][0])
    #     bodem = tuple(contour[contour[:, :, 1].argmax()][0])
    #
    #     l1 = links, rechts
    #     l2 = top, bodem
    #     snijpunt = self.bereken_snijpunt(l1, l2)
    #     frame = cv2.circle(frame, snijpunt, 5, (255, 0, 0), -1)
    #     print(snijpunt)
    #     frame = cv2.line(frame, links, rechts, (0, 255, 0), 1)
    #     frame = cv2.line(frame, top, bodem, (0, 255, 0), 1)
    #
    #     # De punten worden hier getekend voor debugging.
    #     frame = cv2.circle(frame, links, 5, (255, 0, 0), -1)
    #     frame = cv2.circle(frame, rechts, 5, (255, 0, 0), -1)
    #     frame = cv2.circle(frame, top, 5, (255, 0, 0), -1)
    #     frame = cv2.circle(frame, bodem, 5, (255, 0, 0), -1)
    #
    #     # Teken de centroid voor debugging
    #     frame = cv2.circle(frame, centroid, 5, (0, 255, 255), -1)
    #
    #     # Hier onder wordt de afstand van de centroid naar de verste punten berekend.
    #     # De punt die het verst van de centroid ligt is altijd de punt van de tang.
    #     punten = [links, rechts, top, bodem]
    #     afstanden = [self.euclidean_distance(centroid, punt) for punt in punten]
    #
    #     verste_punt_index = np.argmax(afstanden)
    #     verste_punt = punten[verste_punt_index]
    #
    #     return snijpunt

    def verst_liggende_punt(self, contour, centroid, frame):
        """
        Er wordt hier het verste punt van de tang gevonden, wat nodig is voor het object herkenning.
        Er wordt berekend welke van de 4 verste punten van het object het meest van de centroid ligt.
        Dit punt is altijd de punt van de tang.

        Parameters:
            contour: Een contour.
        """
        # Bereken het omhullende rechthoek van de contour
        x, y, w, h = cv2.boundingRect(contour)

        # Vind de vier hoekpunten van het omhullende rechthoek
        links = (x, y + h // 2)
        rechts = (x + w, y + h // 2)
        top = (x + w // 2, y)
        bodem = (x + w // 2, y + h)

        l1 = (links, rechts)
        l2 = (top, bodem)
        snijpunt = self.bereken_snijpunt(l1, l2)

        if snijpunt:
            frame = cv2.circle(frame, snijpunt, 5, (255, 0, 0), -1)

        frame = cv2.line(frame, links, rechts, (0, 255, 0), 1)
        frame = cv2.line(frame, top, bodem, (0, 255, 0), 1)

        # De punten worden hier getekend voor debugging.
        frame = cv2.circle(frame, links, 5, (255, 0, 0), -1)
        frame = cv2.circle(frame, rechts, 5, (255, 0, 0), -1)
        frame = cv2.circle(frame, top, 5, (255, 0, 0), -1)
        frame = cv2.circle(frame, bodem, 5, (255, 0, 0), -1)

        # Teken de centroid voor debugging
        frame = cv2.circle(frame, centroid, 5, (0, 255, 255), -1)

        # Hier onder wordt de afstand van de centroid naar de verste punten berekend.
        # De punt die het verst van de centroid ligt is altijd de punt van de tang.
        punten = [links, rechts, top, bodem]
        afstanden = [self.euclidean_distance(centroid, punt) for punt in punten]

        verste_punt_index = np.argmax(afstanden)
        verste_punt = punten[verste_punt_index]

        return snijpunt

    def euclidean_distance(self, p1, p2):
        """
        Wiskundige berekening die de afstand tussen 2 punten berekent.

        Parameters:
            p1 & p2: Twee punten
        """
        return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def bereken_hoek(self, centroid, angle_line):
        """
        Hier wordt de hoek van de lijn naar het topje van de tang vergeleken met de lijn die tussen de 2 cirkels ligt.
        Heb meerdere lijn-berekeningen geprobeerd, maar daar kwamen telkens ongeldige waardes uit.

        Parameters:
            rect: de minarearect van de contour
            verste_punt: wordt momenteel niet gebruikt (vervangt later self.angle_line), maar is het topje van de tang.
            grijs_frame: Een grijze variant van de frame/image die gebruikt wordt voor object herkenning.
        """
        # Soms worden de waarden doubles en ik weet niet waarom, dus worden ze naar ints gemaakt.
        centroid = [(int(p[0]), int(p[1])) for p in centroid]
        angle_line = [(int(p[0]), int(p[1])) for p in angle_line]

        # Bereken de richtingsvector van de lijnen.
        vector_middle = (centroid[1][0] - centroid[0][0], centroid[1][1] - centroid[0][1])
        vector_angle = (angle_line[1][0] - angle_line[0][0], angle_line[1][1] - angle_line[0][1])

        # Bereken de inwendig product en de grootte van de vector
        dot_product = vector_middle[0] * vector_angle[0] + vector_middle[1] * vector_angle[1]
        magnitude_middle = math.sqrt(vector_middle[0] ** 2 + vector_middle[1] ** 2)
        magnitude_angle = math.sqrt(vector_angle[0] ** 2 + vector_angle[1] ** 2)

        if magnitude_middle == 0 or magnitude_angle == 0:
            return 0.0

        cos_theta = dot_product / (magnitude_middle * magnitude_angle)

        cos_theta = max(min(cos_theta, 1), -1)

        angle_radians = math.acos(cos_theta)

        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

    def bereken_snijpunt(self, lijn1, lijn2):
        """
        Bereken het snijpunt van twee lijnen gegeven door twee punten elk.

        Parameters:
            lijn1: Twee punten die de eerste lijn definiëren.
            lijn2: Twee punten die de tweede lijn definiëren.

        Returns:
            Het snijpunt van de lijnen als tuple (x, y).
            Als de lijnen parallel zijn, retourneer None.
        """
        x1, y1 = lijn1[0]
        x2, y2 = lijn1[1]
        x3, y3 = lijn2[0]
        x4, y4 = lijn2[1]

        # Bereken de determinant
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if denom == 0:
            return None  # Lijnen zijn parallel

        # Bereken het snijpunt
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

        return int(px), int(py)
