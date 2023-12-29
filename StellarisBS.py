from multiprocessing import Pool, cpu_count
from itertools import combinations_with_replacement, combinations, permutations, product


class Fleet:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]


class Ship_model:
    def __init__(self, csv_list) -> None:
        if len(csv_list) == 7:
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
        if len(csv_list) == 11:
            self.name = csv_list[0]
            self.sections = csv_list[1]
            self.size = int(csv_list[2])
            self.power = 0
            self.hull = float(csv_list[3])
            self.armor = float(csv_list[7])
            self.shield = float(csv_list[8])
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
            self.weapon_available_slots = self.weapon_slots.copy()
            self.utility_available_slots = self.utility_slots.copy()
            self.weapon_list = []
            weapon_list = csv_list[9].split(",")
            for wp in weapon_list:
                self.add_weapon(weapon_dict.get(wp))
            self.utility_list = []
            utility_list = csv_list[10].split(",")
            for ut in utility_list:
                self.add_utility(utility_dict.get(ut))

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

    def get_weapons_ready(self, time):
        return [wp for wp in self.weapon_list if wp.ready_to_fire(time)]

    def get_weapon_slot_string(self):
        slot_string = ""
        for key in self.weapon_slots.keys():
            slot_string += str(self.weapon_slots.get(key)) + str(key)
        return slot_string

    def get_utility_slot_string(self):
        slot_string = ""
        for key in self.utility_slots.keys():
            slot_string += str(self.utility_slots.get(key)) + str(key)
        return slot_string

    def get_ship_fullname(self):
        return self.name + "_" + self.sections

    def get_ship_fullname_weapons_utility(self):
        name = self.get_ship_fullname() + "_"
        for i in range(len(self.weapon_list)):
            if i != len(self.weapon_list) - 1:
                name += self.weapon_list[i].get_weapon_fullname() + ","
            else:
                name += self.weapon_list[i].get_weapon_fullname()
        for i in range(len(self.utility_list)):
            if i != len(self.utility_list) - 1:
                name += self.utility_list[i].get_utility_fullname() + ","
            else:
                name += self.utility_list[i].get_utility_fullname()
        return name

    def set_shield(self, value):
        self.shield = value

    def sub_shield(self, value):
        self.set_shield(self.shield - value)

    def set_armor(self, value):
        self.armor = value

    def sub_armor(self, value):
        self.set_armor(self.armor - value)

    def set_hull(self, value):
        self.hull = value

    def sub_hull(self, value):
        self.set_hull(self.hull - value)


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
        self.ut_mods = {"Shield": float(csv_list[11]), "Armor": float(
            csv_list[12]), "Hull": float(csv_list[13])}
        self.skip_mod = {"Shield": float(
            csv_list[14]), "Armor": float(csv_list[15])}
        self.size_mod = {"S": float(csv_list[16]), "M": float(
            csv_list[17]), "L": float(csv_list[18]), "X": float(csv_list[19])}
        self.last_fire = 0

    def get_size_mod(self, size):
        return self.size_mod.get(size)

    def get_ut_mod(self, ut_type):
        return self.ut_mods.get(ut_type)

    def get_skip_mod(self, ut_type):
        return self.skip_mod.get(ut_type)

    def ready_to_fire(self, time):
        if self.last_fire == 0:
            return True
        else:
            return time - self.last_fire >= self.cooldown

    def fire_weapon(self, time):
        self.last_fire = time

    def get_weapon_fullname(self):
        return self.name + "_" + self.size


class Utility:
    def __init__(self, csv_list) -> None:
        self.name = csv_list[0]
        self.type = csv_list[1]
        self.size = csv_list[2]
        self.cost = int(csv_list[3])
        self.power = int(csv_list[4])
        self.value = float(csv_list[5])

    def get_utility_fullname(self):
        return self.name + "_" + self.size


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

# name;sections;size;hull;evasion;weapon_slots;utilities_slot
# name;sections;size;power;hull;armor;shield;evasion;weapons;utilities
# name;sections;size;hull;evasion;weapon_slots;utilities_slot;armor;shield;weapons;utilities


def ship_to_list(object_list):
    sp_list = []
    for ship_list in object_list:
        for ship in ship_list:
            ship_row = []
            ship_row.append(ship.name)
            ship_row.append(ship.sections)
            ship_row.append(ship.size)
            ship_row.append(ship.hull)
            ship_row.append(ship.evasion)
            ship_row.append(ship.get_weapon_slot_string())
            ship_row.append(ship.get_utility_slot_string())
            ship_row.append(ship.armor)
            ship_row.append(ship.shield)
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
    object_dict = {}
    csv_object_list = open_csv(name)
    for object in csv_object_list:
        if type == "Fleet":
            ob = Fleet(object)
            name = ob
        elif type == "ship":
            ob = Ship_model(object)
            name = ob.get_ship_fullname()
        elif type == "weapon":
            ob = Weapon(object)
            name = ob.name + "_" + ob.size
        elif type == "utility":
            ob = Utility(object)
            name = ob.name + "_" + ob.size
        object_dict.update({name: ob})
    return object_dict


def get_ship_list(ship):
    with open("ArmyList.csv", "r", encoding='utf8') as file:
        ship_list = []
        line = file.readline()
        found_ship = True
        while (found_ship):
            line = file.readline()
            line = line.replace("\n", "")
            line_list = line.split(";")
            found_ship = line_list[0] == ship
            if (found_ship):
                ship_list.append(Ship_model(line_list))
    return ship_list


def main():
    # army_list = get_csv_list("FleetList.csv", "Fleet")

    # army = create_army.create_army(
    #     list(ship_dict.values()), list(weapon_dict.values()), list(utility_dict.values()))
    # header = ["name", "sections", "size", "hull", "evasion", "weapon_slots",
    #           "utilities_slot", "armor", "shield", "weapons", "utilities"]
    # write_csv("ArmyList.csv", header, ship_to_list(army))

    # winners_dict = {}
    # for battle in ship_comb:
    #     winner = evaluator.evaluate_combat(battle)
    #     name = winner[0].get_ship_fullname()
    #     if name in winners_dict:
    #         winners_dict.get(name).get("time").append(winner[1])
    #         winners_dict.get(name).get("hull").append(winner[0].hull)
    #         winners_dict.get(name).get("armor").append(winner[0].armor)
    #         winners_dict.get(name).get("shield").append(winner[0].shield)
    #     else:
    #         winners_dict.update({name: {"time": [winner[1]], "hull": [
    #                             winner[0].hull], "armor": [winner[0].armor], "shield": [winner[0].shield]}})
    print(2)


global ship_dict
global weapon_dict
global utility_dict
ship_dict = get_csv_list("ShipList.csv", "ship")
weapon_dict = get_csv_list("WeaponList.csv", "weapon")
utility_dict = get_csv_list("UtilitiesList.csv", "utility")

if __name__ == "__main__":
    main()
