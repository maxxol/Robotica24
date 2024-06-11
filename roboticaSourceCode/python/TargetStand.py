class TargetStand:

    def __init__(self):
        self.geel_onderste = None
        self.geel_bovenste = None

    def maak_masker(self, frame):
        masker = None
        return masker

    def vind_target(self, frame):
        geel_masker = self.maak_masker(frame)
        midden_punt = None
        return midden_punt