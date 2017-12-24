components = [
    component.strip().split('/')
    for component
    in open('components.dat')
]


def bridges(components, current=[], conn='0'):
    for component in components:
        fst, snd = component
        if fst == conn:
            bridge = current + [component]
            yield bridge
            yield from bridges([c for c in components if c != component], bridge, snd)
        elif snd == conn:
            bridge = current + [component]
            yield bridge
            yield from bridges([c for c in components if c != component], bridge, fst)


def strength(bridge):
    return sum(sum(map(int, segment)) for segment in bridge)


print(strength(max(bridges(components), key=lambda x: (len(x), strength(x)))))
