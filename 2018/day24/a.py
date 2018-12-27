import re
from dataclasses import make_dataclass
from itertools import count

Unit = make_dataclass('Unit', 'army id number hp immunities weaknesses dmg dmg_type initiative'.split())
ids = count()


def parse_units(f):
    units = []
    army = next(f)[:-2]
    for line in f:
        if line == '\n':
            break
        base = re.match(r'(\d+) units each with (\d+) hit points ', line)
        line = line[base.span()[1]:]
        number, hp = base.groups()
        m = re.match(r'\((.*)\) ', line)
        immunities = weaknesses = []
        if m:
            extras = m.group(1)
            extras = extras.split('; ')
            for extra in extras:
                if extra.startswith('weak to'):
                    weaknesses = extra[len('weak to '):].split(', ')
                if extra.startswith('immune to '):
                    immunities = extra[len('immune to '):].split(', ')
            line = line[m.span()[1]:]
        combat = re.match(r'with an attack that does (\d+) (\w+) damage at initiative (\d+)', line)
        dmg, dmg_type, initiative = combat.groups()
        units.append(Unit(army,
                          next(ids),
                          int(number),
                          int(hp),
                          immunities,
                          weaknesses,
                          int(dmg),
                          dmg_type,
                          int(initiative)))
    return units


with open('units.dat') as f:
    immune_system = parse_units(f)
    infection = parse_units(f)


def expected_damage(unit, enemy):
    if unit.dmg_type in enemy.immunities:
        ret = 0
    elif unit.dmg_type in enemy.weaknesses:
        ret = unit.number * unit.dmg * 2
    else:
        ret = unit.number * unit.dmg
    return ret


def select_target(attackers, defenders, targets):
    for unit in sorted(attackers,
                       key=lambda u: (int(u.number) * int(u.dmg), int(u.initiative)),
                       reverse=True):

        enemies = sorted((d for d in defenders if d.id not in targets.values() and d.army != unit.army),
                         key=lambda u: (expected_damage(unit, u), u.number * u.dmg, u.initiative),
                         reverse=True)
        if enemies and expected_damage(unit, enemies[0]) > 0:
            targets[unit.id] = enemies[0].id


def play(immune_system, infection):
    while True:
        targets = {}
        print('\nROUND')
        select_target(immune_system, infection, targets)
        select_target(infection, immune_system, targets)

        for attacker in sorted((*immune_system, *infection), key=lambda unit: unit.initiative, reverse=True):
            if attacker.number <= 0:
                continue
            defender = next((unit
                             for unit in (*immune_system, *infection)
                             if unit.id == targets.get(attacker.id, None)),
                            None)
            if defender is None:
                continue

            dealt = expected_damage(attacker, defender) // defender.hp
            print(attacker.army, attacker.id, 'attacks', defender.id, min(defender.number, dealt))
            defender.number -= dealt

        immune_system = [u for u in immune_system if u.number > 0]
        infection = [u for u in infection if u.number > 0]

        if not immune_system:
            return sum(int(n.number) for n in infection)
        elif not infection:
            return sum(int(n.number) for n in immune_system)


assert play(immune_system, infection) == 16090
