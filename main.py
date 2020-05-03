from equipment import Equipment
from equipSystem import EquipSystem

print("Hellow")

AD = Equipment(1, (2 * 10**6))
AS = Equipment(1, (10**6))
ASP = Equipment(2, (10**6))

print(AD.getLamda(), AD.getUniqueVs(87660), AD.getFullVs(87660))
print(AS.getLamda(), AS.getUniqueVs(87660), AS.getFullVs(87660))
print(ASP.getLamda(), ASP.getUniqueVs(87660), ASP.getFullVs(87660))

"""
Un système c'est X equipements (donc un tableau à X entrées ?)
"""
sys = []
sys.append(ASP)
sys.append(AD)

fullSys = EquipSystem(sys)

print("END :", fullSys.getVs(87660))