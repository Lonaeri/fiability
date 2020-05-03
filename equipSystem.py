from equipment import Equipment

class EquipSystem:
    def __init__(self, equipments):
        self.equipments = equipments

    def getVs(self, time):
        result = 1
        for equipment in self.equipments:
            result *= equipment.getFullVs(time)

        return result