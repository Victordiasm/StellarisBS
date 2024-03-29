from copy import deepcopy
from multiprocessing import Pool, cpu_count
from itertools import combinations
import time


class Ship_Result:
    def __init__(self, arglist) -> None:
        self.name = arglist[0]
        self.fullname = arglist[1]
        self.hull = arglist[2]
        self.armor = arglist[3]
        self.shield = arglist[4]


def attack(weapon, ship):
    if ship.size == 1:
        ship_size = "S"
    elif ship.size == 2:
        ship_size = "M"
    elif ship.size == 4:
        ship_size = "L"
    elif ship.size == 8:
        ship_size = "X"
    weapon_damage = weapon.damage_avg * max(
        0, weapon.accuracy - max(0, ship.evasion - weapon.tracking)
    )
    mod_size = weapon.get_size_mod(ship_size)
    mod_shield = weapon.get_ut_mod("Shield")
    mod_skip_shield = weapon.get_skip_mod("Shield")
    mod_armor = weapon.get_ut_mod("Armor")
    mod_skip_armor = weapon.get_skip_mod("Armor")
    mod_hull = weapon.get_ut_mod("Hull")

    shield_mods = mod_shield * mod_size
    armor_mods = mod_armor * mod_size
    hull_mods = mod_hull * mod_size

    shield = ship.shield / shield_mods
    armor = ship.armor / armor_mods
    hull = ship.hull / hull_mods

    shield_damage = 0
    armor_damage = 0
    hull_damage = 0

    if shield > 0:
        shield_damage += weapon_damage * (1 - mod_skip_shield)
        armor_damage += weapon_damage * mod_skip_shield
        if shield >= shield_damage:
            shield -= shield_damage
            shield_damage = 0
        else:
            armor_damage += shield_damage - shield
            shield = 0
    else:
        armor_damage += weapon_damage * (1 - mod_skip_armor)
        hull_damage += weapon_damage * mod_skip_armor

    if armor > 0:
        if armor >= armor_damage:
            armor -= armor_damage
            armor_damage = 0
        else:
            hull_damage += armor_damage - armor
            armor = 0
    else:
        hull_damage += armor_damage

    if shield == 0 and armor == 0:
        if hull >= hull_damage:
            hull -= hull_damage
        else:
            hull = 0
    else:
        if hull_damage > 0:
            if hull >= hull_damage:
                hull -= hull_damage
            else:
                hull = 0

    ship.shield = shield * shield_mods
    ship.armor = armor * armor_mods
    ship.hull = hull * hull_mods


def evaluate_combat(combat):
    shipA = deepcopy(combat[0])
    shipB = deepcopy(combat[1])
    time = 0
    while shipA.hull > 0 and shipB.hull > 0:
        if shipA.hull > 0:
            shipA_weapons = shipA.get_weapons_ready(time)
            for wp in shipA_weapons:
                if shipB.hull > 0:
                    attack(wp, shipB)
                    wp.fire_weapon(time)
        if shipB.hull > 0:
            shipB_weapons = shipB.get_weapons_ready(time)
            for wp in shipB_weapons:
                if shipA.hull > 0:
                    attack(wp, shipA)
                    wp.fire_weapon(time)
        time += tickrt
    if shipA.hull == 0:
        winner = shipB
        loser = shipA
    elif shipB.hull == 0:
        winner = shipA
        loser = shipB
    return {
        "winner": Ship_Result(
            [
                winner.get_ship_fullname(),
                winner.get_ship_fullname_weapons_utility(),
                winner.hull,
                winner.armor,
                winner.shield,
            ]
        ),
        "loser": Ship_Result(
            [
                loser.get_ship_fullname(),
                loser.get_ship_fullname_weapons_utility(),
                loser.hull,
                loser.armor,
                loser.shield,
            ]
        ),
        "time": time,
    }


def init_worker(tickrate):
    global tickrt
    tickrt = tickrate


def evaluate(ship_list, tickrate):
    ship_comb = list(combinations(ship_list, 2))
    cores = cpu_count()
    winner_list = []
    start_time = time.time()
    chunksize = len(ship_comb) // cores // 2
    try:
        with Pool(
            initializer=init_worker,
            initargs=(tickrate,),
            processes=cores,
        ) as pool:
            winner_list = pool.map(evaluate_combat, ship_comb, chunksize=chunksize)
    except Exception as e:
        print(e)

    return winner_list
