components = [
    component.strip().split('/')
    for component
    in open('components.dat')
]


def bridges(components, current=[], conn='0'):
    for component in components:
        fst, snd = component
        if fst == conn:
            out = snd
        elif snd == conn:
            out = fst
        else:
            continue

        bridge = current + [component]
        yield bridge
        yield from bridges([c for c in components if c != component], bridge, out)


def strength(bridge):
    return sum(sum(map(int, segment)) for segment in bridge)


print(max(map(strength, bridges(components))))
