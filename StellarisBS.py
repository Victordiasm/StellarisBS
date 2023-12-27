from itertools import combinations_with_replacement, combinations, permutations, product
from copy import deepcopy
from multiprocessing import Pool, cpu_count
import create_army


class Army:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]


class Ship:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]
        self.sections = csv_list[1]
        self.size = int(csv_list[2])
        self.power = 0
        self.hull = float(csv_list[3])
        self.armor = 0
        self.shield = 0
        self.evasion = float(csv_list[4][0:-1])/100
        self.weapon_slots = {}
        for i in range(0, len(csv_list[5]), 2):
            if (csv_list[5][i+1] in self.weapon_slots):
                self.weapon_slots.update(
                    {csv_list[5][i+1]: self.weapon_slots.get(csv_list[5][i+1]) + int(csv_list[5][i])})
            else:
                self.weapon_slots.update(
                    {csv_list[5][i+1]: int(csv_list[5][i])})
        self.utility_slots = {}
        for i in range(0, len(csv_list[6]), 2):
            if (csv_list[6][i] in self.utility_slots):
                self.utility_slots.update(
                    {csv_list[6][i+1]: self.utility_slots.get(csv_list[6][i+1]) + int(csv_list[6][i])})
            else:
                self.utility_slots.update(
                    {csv_list[6][i+1]: int(csv_list[6][i])})
        self.weapon_list = []
        self.utility_list = []
        self.weapon_available_slots = self.weapon_slots.copy()
        self.utility_available_slots = self.utility_slots.copy()

    def add_weapon(self, weapon):
        self.weapon_list.append(weapon)
        self.weapon_available_slots.update(
            {weapon.size: self.weapon_available_slots.get(weapon.size) - 1})
        self.power += weapon.power

    def add_weapon_list(self, weapon_list):
        for wp_list in weapon_list:
            for wp in wp_list:
                self.add_weapon(wp)

    def add_utility(self, utility):
        self.utility_list.append(utility)
        self.utility_available_slots.update(
            {utility.size: self.utility_available_slots.get(utility.size) - 1})
        self.power += utility.power
        if (utility.type == "Shield"):
            self.shield += utility.value
        elif (utility.type == "Armor"):
            self.armor += utility.value

    def add_utility_list(self, utility_list):
        for ut_list in utility_list:
            for ut in ut_list:
                self.add_utility(ut)

    def get_weapon_slot(self, slot):
        return self.weapon_available_slots.get(slot)

    def get_utility_slot(self, slot):
        return self.utility_available_slots.get(slot)


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
        return (csv_list)


def write_csv(name, header, object_list):
    with open(name, "w", encoding="utf8") as file:
        for s in header:
            file.write(s)
            if header.index(s) == len(header) - 1:
                file.write('\n')
            else:
                file.write(';')
        for row in range(len(object_list)):
            for column in range(len(object_list[row])):
                file.write(str(object_list[row][column]))
                if column == len(object_list[row]) - 1:
                    file.write('\n')
                else:
                    file.write(';')


def ship_to_list(object_list):
    sp_list = []
    for ship_list in object_list:
        for ship in ship_list:
            ship_row = []
            ship_row.append(ship.name)
            ship_row.append(ship.sections)
            ship_row.append(ship.size)
            ship_row.append(ship.power)
            ship_row.append(ship.hull)
            ship_row.append(ship.armor)
            ship_row.append(ship.shield)
            ship_row.append(ship.evasion)
            weapon_list = ""
            for i in range(len(ship.weapon_list)):
                weapon_list += (ship.weapon_list[i].name +
                                "_" + ship.weapon_list[i].size)
                if i != len(ship.weapon_list) - 1:
                    weapon_list += ','
            ship_row.append(weapon_list)
            utility_list = ""
            for i in range(len(ship.utility_list)):
                utility_list += (ship.utility_list[i].name +
                                 "_" + ship.utility_list[i].size)
                if i != len(ship.utility_list) - 1:
                    utility_list += ','
            ship_row.append(utility_list)
            sp_list.append(ship_row)
    return sp_list


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

    army = create_army.create_army(ship_list, weapon_list, utility_list)
    header = ["name", "sections", "size", "power", "hull",
              "armor", "shield", "evasion", "weapons", "utilities"]
    write_csv("ArmyList.csv", header, ship_to_list(army))


if __name__ == "__main__":
    main()
