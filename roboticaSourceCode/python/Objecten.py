class Objecten:
    def __init__(self):
        """
        Klasse structuur van Objecten.

        Parameters:
            self.nieuw (dict): Een lijst van nieuw objecten die zijn herkend.
            self.focus (list): Het object waar op wordt gefocust
        """
        self.nieuw = {}
        self.focus_object = list()

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
                self.focus_object = list(self.focus_object)
                objects = self.nieuw[dichtste_object]
                self.focus_object[2] = objects[2]

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

