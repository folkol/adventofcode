from string import ascii_lowercase

with open('polymer.dat') as f:
    original_units = f.read()

prev_units = None
sizes = {}
for troublemaker in ascii_lowercase:
    units = original_units.replace(troublemaker, "").replace(troublemaker.upper(), "")
    while units != prev_units:
        prev_units = units
        for c in ascii_lowercase:
            react = c + c.upper()
            units = units.replace(react, "")
            react = c.upper() + c
            units = units.replace(react, "")
    sizes[troublemaker] = len(units)
print(min(sizes.values()))
