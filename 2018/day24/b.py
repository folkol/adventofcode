import re
from dataclasses import make_dataclass
from itertools import count

Unit = make_dataclass('Unit',
                      ['army', 'id', 'number', 'hp', 'immunities', 'weaknesses', 'dmg', 'dmg_type', 'initiative'])

ids = count()


def parse_units(f):
    units = []
    army = next(f)[:-2]
    for line in f:
        if line == '\n':
            break
        base = re.match(r'(\d+) units each with (\d+) hit points ', line)
        line = line[base.span()[1]:]
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
        units.append(Unit(army, next(ids), *(int(g) for g in base.groups()), immunities, weaknesses, int(dmg), dmg_type,
                          int(initiative)))
    return units


with open('units.dat') as f:
    immune_system = parse_units(f)
    infection = parse_units(f)


def expected_damage(unit):
    def inner(enemy):
        if unit.dmg_type in enemy.immunities:
            ret = 0, int(enemy.number) * int(enemy.dmg) * 2, int(enemy.initiative)
        elif unit.dmg_type in enemy.weaknesses:
            ret = int(unit.number) * int(unit.dmg) * 2, int(enemy.number) * int(enemy.dmg), int(enemy.initiative)
        else:
            ret = int(unit.number) * int(unit.dmg), int(enemy.number) * int(enemy.dmg), int(enemy.initiative)
        # print(f'{unit.id} would deal {enemy.id} {ret[0]} damage')
        return ret

    return inner


# while True:


def select_target(attackers, defenders, targets):
    for unit in sorted(attackers, key=lambda unit: (int(unit.number) * int(unit.dmg), int(unit.initiative)),
                       reverse=True):

        enemies = sorted((d
                          for d in defenders
                          if d.id not in targets.values()
                          and d.army != unit.army
                          and expected_damage(unit)(d)[0] > 0),
                         key=expected_damage(unit),
                         reverse=True)
        if enemies and expected_damage(unit)(enemies[0])[0] > 0:
            targets[unit.id] = enemies[0].id


def fight(immune_system, infection, boost=0):
    for unit in immune_system:
        unit.dmg += boost
    while True:
        blood_drewn = False
        # print(*immune_system)
        # print(*infection)

        targets = {}
        print('\nROUND', boost)
        select_target(immune_system, infection, targets)
        select_target(infection, immune_system, targets)

        l = sorted((*immune_system, *infection), key=lambda unit: unit.initiative, reverse=True)
        for attacker in l:
            if attacker.number <= 0:
                continue
            defender = next(
                (unit for unit in (*immune_system, *infection) if unit.id == targets.get(attacker.id, None)),
                None)
            if defender is None:
                continue

            dealt = expected_damage(attacker)(defender)[0] // defender.hp
            print(attacker.army, attacker.id, 'attacks', defender.id, min(defender.number, dealt))
            if dealt > 0:
                blood_drewn = True
            defender.number -= dealt

        immune_system = [u for u in immune_system if u.number > 0]
        infection = [u for u in infection if u.number > 0]

        if not immune_system:
            print(sum(int(n.number) for n in infection))
            print(*(n.number for n in infection))
            return False, []
        elif not infection:
            print(sum(int(n.number) for n in immune_system))
            print(*(n.number for n in immune_system))
            return True, immune_system
        elif not blood_drewn:
            return False, []


# fight(immune_system, infection, 1570)

for boost in count():
    defenders = [Unit(u.army, u.id, u.number, u.hp, u.immunities, u.weaknesses, u.dmg, u.dmg_type, u.initiative) for u
                 in immune_system]
    attackers = [Unit(u.army, u.id, u.number, u.hp, u.immunities, u.weaknesses, u.dmg, u.dmg_type, u.initiative) for u
                 in infection]
    win, units = fight(defenders, attackers, boost)
    if win:
        i = sum(int(n.number) for n in units)
        assert i == 8291, immune_system
        print(i)
        break
