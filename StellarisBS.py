import create_army
import evaluator
from os import getcwd
import math
import random
import time

tickrate = 1 / 10


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
            self.evasion = float(csv_list[4][0:-1]) / 100
            if self.evasion == 0:
                print("t")
            self.weapon_slots = {}
            for i in range(0, len(csv_list[5]), 2):
                if csv_list[5][i + 1] in self.weapon_slots:
                    self.weapon_slots.update(
                        {
                            csv_list[5][i + 1]: self.weapon_slots.get(
                                csv_list[5][i + 1]
                            )
                            + int(csv_list[5][i])
                        }
                    )
                else:
                    self.weapon_slots.update({csv_list[5][i + 1]: int(csv_list[5][i])})
            self.utility_slots = {}
            for i in range(0, len(csv_list[6]), 2):
                if csv_list[6][i] in self.utility_slots:
                    self.utility_slots.update(
                        {
                            csv_list[6][i + 1]: self.utility_slots.get(
                                csv_list[6][i + 1]
                            )
                            + int(csv_list[6][i])
                        }
                    )
                else:
                    self.utility_slots.update({csv_list[6][i + 1]: int(csv_list[6][i])})
            self.weapon_list = []
            self.utility_list = []
            self.weapon_available_slots = self.weapon_slots.copy()
            self.utility_available_slots = self.utility_slots.copy()
            self.elo = 1000
        if len(csv_list) == 11:
            self.name = csv_list[0]
            self.sections = csv_list[1]
            self.size = int(csv_list[2])
            self.power = 0
            self.hull = float(csv_list[3])
            self.armor = float(csv_list[7])
            self.shield = float(csv_list[8])
            self.evasion = float(csv_list[4])
            self.weapon_slots = {}
            for i in range(0, len(csv_list[5]), 2):
                if csv_list[5][i + 1] in self.weapon_slots:
                    self.weapon_slots.update(
                        {
                            csv_list[5][i + 1]: self.weapon_slots.get(
                                csv_list[5][i + 1]
                            )
                            + int(csv_list[5][i])
                        }
                    )
                else:
                    self.weapon_slots.update({csv_list[5][i + 1]: int(csv_list[5][i])})
            self.utility_slots = {}
            for i in range(0, len(csv_list[6]), 2):
                if csv_list[6][i] in self.utility_slots:
                    self.utility_slots.update(
                        {
                            csv_list[6][i + 1]: self.utility_slots.get(
                                csv_list[6][i + 1]
                            )
                            + int(csv_list[6][i])
                        }
                    )
                else:
                    self.utility_slots.update({csv_list[6][i + 1]: int(csv_list[6][i])})
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
            self.elo = 1000

    def add_weapon(self, weapon):
        self.weapon_list.append(weapon)
        self.weapon_available_slots.update(
            {weapon.size: self.weapon_available_slots.get(weapon.size) - 1}
        )
        self.power += weapon.power

    def add_weapon_list(self, weapon_list):
        for wp_list in weapon_list:
            for wp in wp_list:
                self.add_weapon(wp)

    def add_utility(self, utility):
        self.utility_list.append(utility)
        self.utility_available_slots.update(
            {utility.size: self.utility_available_slots.get(utility.size) - 1}
        )
        self.power += utility.power
        if utility.type == "Shield":
            self.shield += utility.value
        elif utility.type == "Armor":
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
                name += self.weapon_list[i].get_weapon_fullname() + ","
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

    def get_weapon_list(self):
        weapon_list = [weapon.name for weapon in self.weapon_list]
        return weapon_list

    def get_utility_list(self):
        utility_list = [utility.name for utility in self.utility_list]
        return utility_list


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
        self.tracking = float(csv_list[10])
        self.ut_mods = {
            "Shield": float(csv_list[11]),
            "Armor": float(csv_list[12]),
            "Hull": float(csv_list[13]),
        }
        self.skip_mod = {"Shield": float(csv_list[14]), "Armor": float(csv_list[15])}
        self.size_mod = {
            "S": float(csv_list[16]),
            "M": float(csv_list[17]),
            "L": float(csv_list[18]),
            "X": float(csv_list[19]),
        }
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
    root = getcwd()
    with open("{}\\CSVs\\{}".format(root, name), "r", encoding="utf8") as file:
        text = file.read()
        csv_list = text.split("\n")
        csv_list.pop(0)
        for i in range(len(csv_list)):
            csv_list[i] = csv_list[i].split(";")
        return csv_list


def write_csv(name, header, object_list):
    root = getcwd()
    with open("{}\\CSVs\\{}".format(root, name), "w", encoding="utf8") as file:
        for s in header:
            file.write(s)
            if header.index(s) == len(header) - 1:
                file.write("\n")
            else:
                file.write(";")
        for row in range(len(object_list)):
            for column in range(len(object_list[row])):
                file.write(str(object_list[row][column]))
                if column != len(object_list[row]) - 1:
                    file.write(";")
            if row != len(object_list) - 1:
                file.write("\n")


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
                weapon_list += ship.weapon_list[i].name + "_" + ship.weapon_list[i].size
                if i != len(ship.weapon_list) - 1:
                    weapon_list += ","
            ship_row.append(weapon_list)
            utility_list = ""
            for i in range(len(ship.utility_list)):
                utility_list += (
                    ship.utility_list[i].name + "_" + ship.utility_list[i].size
                )
                if i != len(ship.utility_list) - 1:
                    utility_list += ","
            ship_row.append(utility_list)
            sp_list.append(ship_row)
    return sp_list


def get_csv_dict(name, type):
    object_dict = {}
    csv_object_list = open_csv(name)
    for object in csv_object_list:
        if type == "Fleet":
            ob = Fleet(object)
            name = ob
        elif type == "Ship":
            ob = Ship_model(object)
            name = ob.get_ship_fullname_weapons_utility()
        elif type == "Weapon":
            ob = Weapon(object)
            name = ob.name + "_" + ob.size
        elif type == "Utility":
            ob = Utility(object)
            name = ob.name + "_" + ob.size
        object_dict.update({name: ob})
    return object_dict


def get_ship_list(ship):
    root = getcwd()
    with open("{}\\CSVs\\ArmyList.csv".format(root), "r", encoding="utf8") as file:
        ship_list = []
        line = file.readline()
        found_ship = False
        while not found_ship:
            line = file.readline()
            line = line.replace("\n", "")
            line_list = line.split(";")
            found_ship = line_list[0] == ship
        while found_ship:
            line = file.readline()
            line = line.replace("\n", "")
            line_list = line.split(";")
            found_ship = line_list[0] == ship
            if found_ship:
                ship_list.append(Ship_model(line_list))
    return ship_list


def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


def EloRating(winner, loser):
    Ra = winner.elo
    Rb = loser.elo
    k = 100 * (loser.size / winner.size)
    Pb = Probability(Ra, Rb)
    Pa = Probability(Rb, Ra)
    Ra = Ra + k * (1 - Pa)
    Rb = Rb + k * (0 - Pb)
    winner.elo = round(Ra, 6)
    loser.elo = round(Rb, 6)


def main():
    global weapon_dict
    weapon_dict = get_csv_dict("WeaponList.csv", "Weapon")
    global utility_dict
    utility_dict = get_csv_dict("UtilitiesList.csv", "Utility")

    ship_dict = get_csv_dict("ShipList.csv", "Ship")
    army = create_army.create_army(
        list(ship_dict.values()),
        list(weapon_dict.values()),
        list(utility_dict.values()),
    )

    header = [
        "name",
        "sections",
        "size",
        "hull",
        "evasion",
        "weapon_slots",
        "utilities_slot",
        "armor",
        "shield",
        "weapons",
        "utilities",
    ]

    write_csv("ArmyList.csv", header, ship_to_list(army))

    ship_name_list = ["Corvette", "Frigate", "Destroyer", "Cruiser", "Battleship"]
    # ship_name_list = ["Corvette", "Frigate"]
    for ship_name in ship_name_list:
        start_time = time.time()
        print("Starting Evaluation of {}".format(ship_name))
        ship_list = get_ship_list(ship_name)

        combat_list = evaluator.evaluate(ship_list, tickrate)

        print("Finished Evaluation of {}".format(ship_name))
        end_time = time.time()
        print("Processing Time:", end_time - start_time)
        result_ship_dict = {}
        for ship in ship_list:
            result_ship_dict.update({ship.get_ship_fullname_weapons_utility(): ship})

        for combat in combat_list:
            winner_name = combat.get("winner").fullname
            loser_name = combat.get("loser").fullname
            if winner_name != loser_name:
                winner = result_ship_dict.get(winner_name)
                loser = result_ship_dict.get(loser_name)
                EloRating(winner, loser)

        sorted_ship_dict = sorted(
            result_ship_dict.items(), key=lambda x: x[1].elo, reverse=True
        )
        ship_header = [
            "elo",
            "name",
            "sections",
            "size",
            "hull",
            "armor",
            "shield",
            "evasion",
            "weapons",
            "utilities",
        ]
        result_list = []
        for ship_tuple in sorted_ship_dict:
            ship = ship_tuple[1]
            result = [
                ship.elo,
                ship.name,
                ship.sections,
                ship.size,
                ship.hull,
                ship.armor,
                ship.shield,
                ship.evasion,
                ship.get_weapon_list(),
                ship.get_utility_list(),
            ]
            result_list.append(result)
        write_csv("combat_result_{}.csv".format(ship_name), ship_header, result_list)

    return


if __name__ == "__main__":
    main()
