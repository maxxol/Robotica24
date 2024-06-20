import math
import cv2
import numpy as np
from Objecten import Objecten


class KleurenStand:
    def __init__(self):
        """
        De constructor voor de KleurenStand klasse.

        Variabelen:
            self.objecten : (Objecten()): De klasse bevat een lijst met herkende objecten en het object waarop gefocust wordt.
            self.kleur_onderste/bovenste (np.array): Dit zijn de min-max hsv waarden voor de 5 kleuren.
            self.kernel (np.ones): Kernel voor kleurherkenning
            self.min_area (int): De minimale grootte dat geëist wordt van een contour
        """
        self.objecten = Objecten()

        self.rood_onderste = np.array([0, 150, 100], np.uint8)
        self.rood_bovenste = np.array([10, 255, 200], np.uint8)
        self.rood_onderste2 = np.array([170, 150, 100], np.uint8)
        self.rood_bovenste2 = np.array([180, 255, 180], np.uint8)

        self.groen_onderste = np.array([35, 50, 50], np.uint8)
        self.groen_bovenste = np.array([70, 255, 255], np.uint8)

        self.blauw_onderste = np.array([100, 100, 100], np.uint8)
        self.blauw_bovenste = np.array([130, 255, 255], np.uint8)

        self.magenta_onderste = np.array([150, 50, 180], np.uint8)
        self.magenta_bovenste = np.array([175, 255, 255], np.uint8)

        # self.grijs_onderste = np.array([0, 0, 0], np.uint8)
        # self.grijs_bovenste = np.array([160, 30, 200], np.uint8)

        self.kernel = np.ones((5, 5), "uint8")

        self.min_area = 300

        # Allemaal voor debugging:

        self.circles = None

        self.frame = None

        self.middle_line = []

        self.rows = None

        self.cols = None

        self.middle_line = None
        self.angle_line = None
        self.middle_point = None

    def detect(self, frame, kleur, focus_object):
        """
        De main van de KleurenStand.
        Hierin staan alle methoden gebruik voor de kleur en object herkenning

        Parameters:
            frame (string/image): Het frame bevat een pad naar een afbeelding of geeft een frame mee van de camera.
            kleur (string): De kleur die van het object dat herkent moet worden.
        """

        # Als je de objectherkenning wilt testen op een image path, dan kan je dit hieronder gebruiken. Anders #.
        # frame = cv2.imread(frame)
        # scale_factor = 0.8
        # frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)
        # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        if focus_object:
            self.objecten.focus_object = focus_object

        self.frame = frame

        masker, grijs_frame = self.maak_masker(self.frame, kleur)

        if not isinstance(masker, np.ndarray):
            return

        self.vind_objecten(masker, kleur, grijs_frame)

        if len(self.objecten.nieuw) == 0 or None:
            self.objecten.verwijder_object()
        else:
            focus_object = self.objecten.update_positie()
            self.teken_contouren(frame)
            return focus_object
        return

        # self.teken_contouren(self.objecten.oud, self.frame)

        # Geeft een mask terug voor debugging
        # return self.masks['grijs']

    def maak_masker(self, frame, kleur):
        """
        In deze methode wordt voor de kleur een masker aangemaakt.
        Voor de maskers wordt er een hsv_frame gebruikt en de grijs_frame wordt later gebruikt voor object herkenning.

        Parameters:
            frame (string/image): Het frame bevat een pad naar een afbeelding of geeft een frame mee van de camera.
            kleur (string): De kleur die van het object dat herkent moet worden.
        """

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        grijs_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        match kleur:
            case 'rood':
                rood_mask1 = cv2.inRange(hsv_frame, self.rood_onderste, self.rood_bovenste)
                rood_mask2 = cv2.inRange(hsv_frame, self.rood_onderste2, self.rood_bovenste2)
                rood_mask = cv2.bitwise_or(rood_mask1, rood_mask2)
                rood_mask = cv2.dilate(rood_mask, self.kernel)

                magenta_mask = cv2.inRange(hsv_frame, self.magenta_onderste, self.magenta_bovenste)
                magenta_mask = cv2.dilate(magenta_mask, self.kernel)

                magenta_count = cv2.countNonZero(magenta_mask)
                rood_count = cv2.countNonZero(rood_mask)

                # cv2.imshow("redmask", rood_mask)
                # cv2.waitKey(0)

                self.mask = rood_mask

                if magenta_count > rood_count:
                    return 'none', grijs_frame
                else:
                    return rood_mask, grijs_frame

                # cv2.imshow("fasf", rood_mask)
                # cv2.waitKey(0)
            case 'groen':
                groen_mask = cv2.inRange(hsv_frame, self.groen_onderste, self.groen_bovenste)
                groen_mask = cv2.dilate(groen_mask, self.kernel)
                return groen_mask, grijs_frame
            case 'blauw':
                blauw_mask = cv2.inRange(hsv_frame, self.blauw_onderste, self.blauw_bovenste)
                blauw_mask = cv2.dilate(blauw_mask, self.kernel)
                return blauw_mask, grijs_frame
            case 'magenta':
                # moet nog aangepast worden naar magenta.
                magenta_mask = cv2.inRange(hsv_frame, self.magenta_onderste, self.magenta_bovenste)
                magenta_mask = cv2.dilate(magenta_mask, self.kernel)

                return magenta_mask, grijs_frame

    def vind_objecten(self, masker, kleur, grijs_frame):
        """
        Eerst worden er gezocht naar contouren die groter zijn dan de minimale grootte
        Daarna wordt er object herkenning toegepast,
        eerst door de punt van de tang te vinden en dat dan te vergelijken met de 2 cirkels die de tang bevat.

        Parameters:
            masker: Het masker wordt gebruikt om contouren te vinden van bepaalde kleuren.
            kleur (string): De kleur die van het object dat herkent moet worden.
            grijs_frame (image): Een grijze variant van de frame/image die gebruikt wordt voor object herkenning.
        """

        contours, hierarchy = cv2.findContours(masker, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for pic, contour in enumerate(contours):
            if hierarchy[0][pic][3] == -1:
                area = cv2.contourArea(contour)

                if area > self.min_area:
                    rect = cv2.minAreaRect(contour)
                    type_object = self.object_herkenning(rect, contour, grijs_frame)
                    if type_object is not None and type_object != "idk":
                        cx, cy = self.centroid(contour)
                        vx, vy, x, y = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
                        #print(vx, vy)

                        # Calculate two points on the line to draw the line
                        lefty = int((-x * vy / vx) + y)
                        righty = int(((self.frame.shape[1] - x) * vy / vx) + y)
                        
                        # Draw the line
                        cv2.line(self.frame, (self.frame.shape[1] - 1, righty), (0, lefty), (0, 255, 0), 2)
                        self.frame = cv2.circle(self.frame, (cx, cy), 5, (255, 0, 0), -1)
                        if self.objecten.nieuw != {}:
                            last_item = next(reversed(self.objecten.nieuw))
                            new_item = int(last_item) + 1
                            self.objecten.nieuw.update({new_item: (type_object, kleur, rect, (cx, cy), (vx, vy, x, y))})
                        else:
                            self.objecten.nieuw.update({1: (type_object, kleur, rect, (cx, cy), (vx, vy, x, y))})

    def centroid(self, contour):

        m = cv2.moments(contour)
        if m['m00'] != 0:
            cx = int(m['m10'] / m['m00'])
            cy = int(m['m01'] / m['m00'])
        else:
            cx = 0
            cy = 0
        return cx, cy

    def verst_liggende_punt(self, contour):
        """
        Er wordt hier het verste punt van de tang gevonden, wat nodig is voor het object herkenning.
        Er wordt berekend welke van de 4 verste punten van het object het meest van de middenpunt ligt.
        Dit punt is altijd de punt van de tang.

        Parameters:
            contour: Een contour.
        """
        # De vier variabelen hieronder zijn de verste punten gevonden in de contour van de tang.
        links = tuple(contour[contour[:, :, 0].argmin()][0])
        rechts = tuple(contour[contour[:, :, 0].argmax()][0])
        top = tuple(contour[contour[:, :, 1].argmin()][0])
        bodem = tuple(contour[contour[:, :, 1].argmax()][0])

        # De punten worden hier getekend voor debugging.
        self.frame = cv2.circle(self.frame, links, 5, (255, 0, 0), -1)
        self.frame = cv2.circle(self.frame, rechts, 5, (255, 0, 0), -1)
        self.frame = cv2.circle(self.frame, top, 5, (255, 0, 0), -1)
        self.frame = cv2.circle(self.frame, bodem, 5, (255, 0, 0), -1)

        # Gebruik de gegeven middenpunt
        middenpunt = self.middle_point

        # Teken de middenpunt voor debugging
        self.frame = cv2.circle(self.frame, middenpunt, 5, (0, 255, 255), -1)

        # Hier onder wordt de afstand van de middenpunt naar de verste punten berekend.
        # De punt die het verst van de middenpunt ligt is altijd de punt van de tang.
        punten = [links, rechts, top, bodem]
        afstanden = [self.euclidean_distance(middenpunt, punt) for punt in punten]

        verste_punt_index = np.argmax(afstanden)
        verste_punt = punten[verste_punt_index]

        return verste_punt

    def euclidean_distance(self, p1, p2):
        """
        Wiskundige berekening die de afstand tussen 2 punten berekent.
        
        Parameters:
            p1 & p2: Twee punten
        """
        return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def object_herkenning(self, rect, contour, grijs_frame):
        """
        Hier wordt de objectherkenning gedaan.
        Er wordt binnen de regio van de contour (x/y-1/2) gezocht naar cirkels.
        Als de contour 2 cirkels bevat, wordt er een lijn getekend tussen het middenpunt van de 2 cirkels.
        De hoek van de lijn die getrokken wordt uit het middenpunt naar de top van de tang wordt berekend.
        Vanuit die hoek kunnen we concluderen als het een rechte of kromme tang is.

        Parameters:
            rect: de minarearect van de contour
            verste_punt: wordt momenteel niet gebruikt (vervangt later self.angle_line), maar is het topje van de tang.
            grijs_frame: Een grijze variant van de frame/image die gebruikt wordt voor object herkenning.
            contour: De contour.
        """
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)

        # # Min-max x en y van de contour box
        # x1 = np.min([value for value in box[:, 0] if value >= 0])
        # x2 = np.max(box[:, 0])
        # y1 = np.min([value for value in box[:, 1] if value >= 0])
        # y2 = np.max(box[:, 1])

        
        # # Dit is de 'region of interest' aka de contour area van de afbeelding.
        # # Er worden alleen voor cirkels gezocht binnen de roi.
        # roi = grijs_frame[y1:y2, x1:x2]

        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # This is the 'region of interest' around the object within the bounding box of the contour.
        roi = grijs_frame[y:y+h, x:x+w]

        # Blur voor herkenning
        roi_blurred = cv2.blur(roi, (3, 3))

        cv2.imwrite(r'/home/rob8/Robotica24/roboticaSourceCode/python/pyIMG/roi_blurred.jpg', roi_blurred)

        # Hier worden de circles gedetecteerd
        # Je kan meerdere variabelen meegeven om de detectie nauwkeuriger/losser te maken.
        circles = cv2.HoughCircles(
            roi_blurred,
            cv2.HOUGH_GRADIENT,
            1, 20,
            param1=50,
            param2=40,
            minRadius=1,
            maxRadius=40
        )

        if circles is None:
            return
        if circles.shape[1] >= 2:
            # De positie van de cirkels in de contour moet omgerekend worden naar hen positie in de originele afbeelding
            circles_global = circles[0] + np.array([x, y, 0])
            circles = np.uint16(np.around(circles_global))
            # self.circles wordt gebruikt voor debugging, anders gewoon cirkels.
            self.circles = circles
            center1 = circles[0][:2]
            center2 = circles[1][:2]
            # Zelfde voor deze variabelen
            self.middle_line = (center1, center2)
            self.middle_point = (center1 + center2) // 2

            verste_punt = self.verst_liggende_punt(contour)
            self.angle_line = verste_punt

            # Angle is de hoek tussen het punt van het object naar het middenpunt van de cirkels
            angle = self.bereken_hoek(self.middle_line, (self.middle_point, self.angle_line))

            # Als de angle 85-95 ligt,
            # is het een rechte tang. Anders een kromme tang.
            # Eventueel zou het aantal graden van de kromme tang nauwkeuriger gemaakt kunnen worden.
            if 85 <= angle <= 95:
                #print("rechte tang" + " " + str(angle))
                return "rechteTang"
            if 85 > angle or angle > 95:
                print("kromme tang" + " " + str(angle))
                return "krommeTang"
            else:
                # print("idk")
                return "idk"

    def bereken_hoek(self, middle_line, angle_line):
        """
        Hier wordt de hoek van de lijn naar het topje van de tang vergeleken met de lijn die tussen de 2 cirkels ligt.
        Heb meerdere lijn-berekeningen geprobeerd, maar daar kwamen telkens ongeldige waardes uit.


        Parameters:
            rect: de minarearect van de contour
            verste_punt: wordt momenteel niet gebruikt (vervangt later self.angle_line), maar is het topje van de tang.
            grijs_frame: Een grijze variant van de frame/image die gebruikt wordt voor object herkenning.
        """
        # Soms worden de waarden doubles en ik weet niet waarom, dus worden ze naar ints gemaakt.
        middle_line = [(int(p[0]), int(p[1])) for p in middle_line]
        angle_line = [(int(p[0]), int(p[1])) for p in angle_line]

        # Bereken de richtingsvector van de lijnen.
        vector_middle = (middle_line[1][0] - middle_line[0][0], middle_line[1][1] - middle_line[0][1])
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

    def teken_contouren(self, frame):
        """
        Hier worden de contouren van de objecten getekend, plus de lijnen die gebruikt worden tijdens de berekeningen.
        Voor de laatste versie van het project zal deze functie niet gebruikt worden.

        Parameters:
            objecten: lijst met alle objecten die herkend zijn.
            frame: het plaatje/frame van de camera.
        """

        rect = self.objecten.focus_object[2]
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        kleur = self.get_kleur(self.objecten.focus_object[1])
        self.frame = cv2.drawContours(frame, [box], -1, kleur, 2)
        if self.circles is not None:
            for circle in self.circles:
                self.frame = cv2.circle(frame, (circle[0], circle[1]), circle[2], (255, 0, 0), 1)

        cv2.line(frame, self.middle_line[0], self.middle_line[1], (255, 0, 0), 1)
        cv2.line(frame, self.middle_point, self.angle_line, (255, 0, 0), 1)
        center = tuple(map(int, rect[0]))
        # cv2.putText(frame, str(key) + "" + str(value), (center[0], center[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, kleur)
        cv2.putText(frame, str(self.objecten.focus_object[0]) + " " + str(self.objecten.focus_object[4][0]) + str(self.objecten.focus_object[4][1]), (center[0], center[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, kleur)

    def get_kleur(self, kleur):
        """
        Wordt gebruikt voor het ophalen van de rgb waardes van de opgegeven kleuren, tijdens het tekenen van de contouren
        Parameters:
            kleur: De kleur.
        """
        match kleur:
            case 'rood':
                return 0, 0, 255
            case 'groen':
                return 0, 255, 0
            case 'blauw':
                return 255, 0, 0
            case 'magenta':
                return 0, 255, 255
        return 255, 255, 255
