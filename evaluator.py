tickrate = 100


def attack(weapon, ship):
    if ship.size == 1:
        ship_size = "S"
    elif ship.size == 2:
        ship_size = "M"
    elif ship.size == 4:
        ship_size = "L"
    elif ship.size == 8:
        ship_size = "X"
    weapon_damage = weapon.damge_avg
    mod_size = weapon.get_size_mod(ship_size)
    mod_shield = weapon.get_ut_mod("Shield")
    mod_skip_shield = weapon.get_skip_mod("Shield")
    mod_armor = weapon.get_ut_mod("Armor")
    mod_skip_armor = weapon.get_skip_mod("Armor")
    mod_hull = weapon.get_ut_mod("Hull")

    leftover_damage_shield = 0
    leftover_damage_armor = 0
    if ship.hull > 0:
        if ship.armor > 0:
            if ship.shield > 0:
                shield_damage = weapon_damage * mod_shield * \
                    mod_size * (1 - mod_skip_shield)
                leftover_damage_shield = shield_damage * mod_skip_shield
                if ship.shield > shield_damage:
                    ship.shield -= shield_damage
                else:
                    ship.shield = 0
                    leftover_damage_shield += (shield_damage -
                                               ship.shield)/(mod_shield * mod_size)
            armor_damage = leftover_damage_shield
            armor_damage += weapon_damage * mod_armor * \
                mod_size * (1 - mod_skip_armor)
            leftover_damage_armor = armor_damage * mod_skip_armor
            if ship.armor > armor_damage:
                ship.armor -= armor_damage
            else:
                ship.armor = 0
                leftover_damage_armor += (armor_damage -
                                          ship.armor)/(mod_armor * mod_size)
        hull_damage = leftover_damage_armor
        hull_damage += weapon_damage * mod_hull * mod_size
        if ship.hull > hull_damage:
            ship.hull -= hull_damage
        else:
            ship.hull = 0


def evaluate_combat(shipA, shipB):
    time = 0
    while shipA.hull > 0 and shipB.hull > 0:
        shipA_weapons = shipA.get_weapons_ready(time)
        shipB_weapons = shipB.get_weapons_ready(time)
        for wp in shipA_weapons:
            attack(wp, shipB)
        for wp in shipB_weapons:
            attack(wp, shipA)
        time += tickrate
    if shipA.hull == 0:
        winner = shipB
    elif shipB == 0:
        winner = shipA
    return winner
