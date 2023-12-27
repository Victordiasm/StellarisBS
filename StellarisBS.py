class Army:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]


class Ship:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]
        self.sections = csv_list[1]
        self.size = int(csv_list[2])
        self.hull = float(csv_list[3])
        self.evasion = float(csv_list[4][0:-1])/100
        self.weapon_slots = {}
        for i in range(0, len(csv_list[5]), 2):
            if(csv_list[5][i+1] in self.weapon_slots):
                self.weapon_slots.update({csv_list[5][i+1]:self.weapon_slots.get(csv_list[5][i+1]) + int(csv_list[5][i])})
            else:
                self.weapon_slots.update({csv_list[5][i+1]:int(csv_list[5][i])})           
        self.utilities_slots = {}
        for i in range(0, len(csv_list[6]), 2):
            if(csv_list[6][i] in self.utilities_slots):
                self.utilities_slots.update({csv_list[6][i+1]:self.utilities_slots.get(csv_list[6][i+1]) + int(csv_list[6][i])})
            else:
                self.utilities_slots.update({csv_list[6][i+1]:int(csv_list[6][i])})
        self.weapon_list = []
        self.utilities_list = []


class Weapon:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]
        self.type = csv_list[1]
        self.size = csv_list[2]
        self.cost = int(csv_list[3])
        self.power = int(csv_list[4])
        self.damage_range = csv_list[5]
        self.damage_avg = float(csv_list[6])
        self.cooldown = float(csv_list[7])
        self.range = csv_list[8]
        self.accuracy = float(csv_list[9])
        self.traking = float(csv_list[10])
        self.shield_mod = float(csv_list[11])
        self.armor_mod = float(csv_list[12])
        self.hull_mod = float(csv_list[13])
        self.skip_shield = float(csv_list[14])
        self.skip_armor = float(csv_list[15])
        self.sizeS_mod = float(csv_list[16])
        self.sizeM_mod = float(csv_list[17])
        self.sizeL_mod = float(csv_list[18])
        self.sizeX_mod = float(csv_list[19])


class Utility:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]
        self.type = csv_list[1]
        self.size = csv_list[2]
        self.cost = int(csv_list[3])
        self.power = int(csv_list[4])
        self.value = float(csv_list[5])


def open_csv(name):
    with open(name, 'r', encoding='utf8') as file:
        text = file.read()
        csv_list = text.split('\n')
        csv_list.pop(0)
        for i in range(len(csv_list)):
            csv_list[i] = csv_list[i].split(';')
        return(csv_list)


def get_csv_list(name, type):
    object_list = []
    csv_object_list = open_csv(name)
    for object in csv_object_list:
        if type == "army":
            object_list.append(Army(object))
        elif type == "ship":
            object_list.append(Ship(object))
        elif type == "weapon":
            object_list.append(Weapon(object))
        elif type == "utility":
            object_list.append(Utility(object))        
    return object_list




def main():
    army_list = get_csv_list("ArmyList.csv", "army")
    ship_list = get_csv_list("ShipList.csv", "ship")
    weapon_list = get_csv_list("WeaponList.csv", "weapon")
    utility_list = get_csv_list("UtilitiesList.csv", "utility")


if __name__ == "__main__":
    main()

