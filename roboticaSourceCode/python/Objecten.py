class Objecten:
    def __init__(self):
        """
        Klasse structuur van Objecten.

        Parameters:
            self.nieuw (dict): Een lijst van nieuw objecten die zijn herkend.
            self.focus (list): Het object waar op wordt gefocust
        """
        self.nieuw = {}
        self.focus_object = []

    def update_positie(self):
        """
        Hier worden alle nieuwe objecten vergeleken met het self.focus_object.
        Het object die het dichtsbij ligt wordt opgeslagen als het focus_object.
        In het geval dat er nog geen focus_object is dan wordt er een andere methode aangeroepen.

        """
        if self.focus_object != [] and self.nieuw:
            dichtste_object = None
            dichtste_afstand = float('inf')

            for key_nieuw, value_nieuw in self.nieuw.items():
                distance = self.object_afstand(value_nieuw[2], self.focus_object[2])
                if distance < dichtste_afstand and value_nieuw[1] == self.focus_object[1]:
                    dichtste_afstand = distance
                    dichtste_object = key_nieuw

            if dichtste_object is not None:
                self.focus_object = self.nieuw[dichtste_object]

        if not self.focus_object:
            self.verander_focus()

        self.nieuw = {}
        return self.focus_object

    def verander_focus(self):
        """
        Als er geen focus_object is, dan vergelijkt hij alle contouren met het middenpunt van het scherm.
        Het object dat het dichtste bij het middenpunt ligt, wordt het nieuwe focus_object.

        """
        middel_punt = (480 // 2, 360 // 2)

        dichtste_object = None
        dichtste_afstand = float('inf')

        for key_nieuw, value_nieuw in self.nieuw.items():
            distance = self.object_afstand(value_nieuw[2], ((middel_punt), (0, 0), 0))
            if distance < dichtste_afstand:
                dichtste_afstand = distance
                dichtste_object = key_nieuw

        if dichtste_object is not None:
            self.focus_object = self.nieuw[dichtste_object]
        return self.focus_object

    def object_afstand(self, rect1, rect2):
        """
        Wiskundige berekening die de afstand tussen 2 contouren berekent.

        Parameters:
            rect1 & rect2: Twee punten
        """
        (x1, y1), _, _ = rect1
        (x2, y2), _, _ = rect2

        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def verwijder_object(self):
        """

        Als er geen objecten worden gevonden van een bepaalde kleur, worden alle variabelen leeggehaald.

        """
        self.nieuw = {}
        self.focus_object = []
        return

# class Objecten:
#     def __init__(self):
#         self.oud = {}
#         self.nieuw = {}
#
#     def update_positie(self):
#         # Er wordt geen onderscheid gemaakt van kleur, vandaar dat hij niet goed 2 verschillende kleuren tegelijk
#         # kan tekenen.
#
#         if self.oud != {}:
#             for key_nieuw, value_nieuw in list(self.nieuw.items()):
#                 closest_key = None
#                 closest_distance = float('inf')
#
#                 for key_oud, value_oud in list(self.oud.items()):
#                     distance = self.object_distance((value_nieuw[2]), (value_oud[2]))
#                     if distance < closest_distance and value_nieuw[1] == value_oud[1]:
#                         closest_distance = distance
#                         closest_key = key_oud
#
#                 if closest_key is not None:
#                     self.oud[closest_key] = value_nieuw
#                 else:
#                     last_item = next(reversed(self.nieuw))
#                     new_item = int(last_item) + 1
#                     self.oud.update({new_item: (value_nieuw[0], value_nieuw[1], value_nieuw[2], value_nieuw[3])})
#         else:
#             self.oud = self.nieuw
#             self.nieuw = {}
#             return self.oud
#
#         self.nieuw = {}
#         return self.oud
#
#     def object_distance(self, rect1, rect2):
#         # Extract the center points from the rectangles
#         (x1, y1), (w1, h1), angle1 = rect1
#         (x2, y2), (w2, h2), angle2 = rect2
#
#         # Calculate the Euclidean distance between the two center points
#         return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
#
#     def remove_object(self, kleur):
#         if self.oud:
#             keys_to_remove = [key for key, value in self.oud.items() if value[1] == kleur]
#             for key in keys_to_remove:
#                 self.oud.pop(key)
#         return
#
