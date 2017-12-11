steps = open('path.dat').read().split(",")

x = 0
y = 0
z = 0
for step in steps:
    if step == 'nw':
        x -= 1
        y += 1
    elif step == 'n':
        y += 1
        z -= 1
    elif step == 'ne':
        z -= 1
        x += 1
    elif step == 'se':
        x += 1
        y -= 1
    elif step == 's':
        y -= 1
        z += 1
    elif step == 'sw':
        x -= 1
        z += 1
    else:
        raise 'Unknown step' + step

print(max(abs(x), abs(y), abs(z)))
