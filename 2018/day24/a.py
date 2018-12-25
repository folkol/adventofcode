import re
from dataclasses import make_dataclass

Unit = make_dataclass('Unit', ['number', 'hp', 'extras', 'dmg', 'dmg_type', 'initiative'])


def parse_units(f):
    units = []
    next(f)
    for line in f:
        if line == '\n':
            break
        base = re.match(r'(\d+) units each with (\d+) hit points ', line)
        line = line[base.span()[1]:]
        m = re.match(r'\((.*)\) ', line)
        if m:
            extras = m.group(1)
            line = line[m.span()[1]:]
        else:
            extras = None
        combat = re.match(r'with an attack that does (\d+) (\w+) damage at initiative (\d+)', line)
        units.append(Unit(*base.groups(), extras, *combat.groups()))
    return units


with open('units.dat') as f:
    immune_system = parse_units(f)
    infection = parse_units(f)

print('Immune System:')
for unit in immune_system:
    print(f'{unit.number} units each with {unit.hp} hit points ', end='')
    if unit.extras:
        print(f'({unit.extras}) ', end='')
    print(f'with an attack that does {unit.dmg} {unit.dmg_type} damage at initiative {unit.initiative}')
print()
print('Infection:')
for unit in infection:
    print(f'{unit.number} units each with {unit.hp} hit points ', end='')
    if unit.extras:
        print(f'({unit.extras}) ', end='')
    print(f'with an attack that does {unit.dmg} {unit.dmg_type} damage at initiative {unit.initiative}')
