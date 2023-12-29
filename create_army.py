from itertools import combinations_with_replacement, combinations, permutations, product
from copy import deepcopy
from multiprocessing import Pool, cpu_count
import StellarisBS


def create_ship(raw_ship):
    weapon_slot_key_list = raw_ship.weapon_slots.keys()
    utility_slot_key_list = raw_ship.utility_slots.keys()
    weapon_comb_list = []
    for key in weapon_slot_key_list:
        slots = raw_ship.get_weapon_slot(key)
        temp_list = [tmp for tmp in wp_list if tmp.size == key]
        comb_list = list(combinations_with_replacement(temp_list, slots))
        weapon_comb_list.append(comb_list)
    ship_wp_comb = []
    for element in product(*weapon_comb_list):
        ship_wp_comb.append(element)

    utility_comb_list = []
    for key in utility_slot_key_list:
        slots = raw_ship.get_utility_slot(key)
        temp_list = [ut for ut in ut_list if ut.size == key]
        comb_list = list(combinations_with_replacement(temp_list, slots))
        utility_comb_list.append(comb_list)
    ship_ut_comb = []
    for element in product(*utility_comb_list):
        ship_ut_comb.append(element)
    ship_product = list(product(ship_wp_comb, ship_ut_comb))
    army_list = []
    for sp in ship_product:
        ship = deepcopy(raw_ship)
        ship.add_weapon_list(sp[0])
        ship.add_utility_list(sp[1])
        army_list.append(ship)
    print("Finished ship -", raw_ship.name)
    return army_list


def init_worker(weapon_list, utility_list):
    # declare scope of a new global variable
    global wp_list
    global ut_list
    # store argument in the global variable for this process
    wp_list = weapon_list
    ut_list = utility_list


def create_army(ship_list, weapon_list, utility_list):
    cores = cpu_count()
    with Pool(initializer=init_worker, initargs=(weapon_list, utility_list), processes=cores) as pool:
        army_list = pool.map(create_ship, ship_list, chunksize=1)
    return army_list


def main():
    ship_dict = StellarisBS.get_csv_list("ShipList.csv", "ship")
    weapon_dict = StellarisBS.get_csv_list("WeaponList.csv", "weapon")
    utility_dict = StellarisBS.get_csv_list("UtilitiesList.csv", "utility")

    army = create_army(
        list(ship_dict.values()), list(weapon_dict.values()), list(utility_dict.values()))
    header = ["name", "sections", "size", "hull", "evasion", "weapon_slots",
              "utilities_slot", "armor", "shield", "weapons", "utilities"]
    StellarisBS.write_csv("ArmyList.csv", header,
                          StellarisBS.ship_to_list(army))


if __name__ == "__main__":
    main()
