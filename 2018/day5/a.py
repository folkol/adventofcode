from string import ascii_lowercase

with open('polymer.dat') as f:
    units = f.read()

prev_units = None
while units != prev_units:
    prev_units = units
    for c in ascii_lowercase:
        react = c + c.upper()
        units = units.replace(react, "")
        react = c.upper() + c
        units = units.replace(react, "")
print(len(units))
