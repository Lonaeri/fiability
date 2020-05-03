import math

class Equipment:
    def __init__(self, nbEquipment, mtbf):
        self.nbEquipment = nbEquipment
        self.mtbf = mtbf

    """
    For one equipement
    """
    def getLamda(self): 
        return 1.0 / self.mtbf

    def getUniqueVs(self, time):
        return math.exp(-self.getLamda() * time)

    def getFullVs(self, time):
        return 1 - ((1 - self.getUniqueVs(time)) ** self.nbEquipment)