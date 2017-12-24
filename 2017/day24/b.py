components = [
    component.strip().split('/')
    for component
    in open('components.dat')
]


def bridges(components, current=[], conn='0'):
    for component in components:
        fst, snd = component
        if fst == conn:
            next_conn = snd
        elif snd == conn:
            next_conn = fst
        else:
            continue

        bridge = current + [component]
        yield bridge
        yield from bridges([c for c in components if c != component], bridge, next_conn)


def strength(bridge):
    return sum(sum(map(int, segment)) for segment in bridge)


def long_and_strong(bridge):
    return len(bridge), strength(bridge)


longest_bridge = max(bridges(components), key=long_and_strong)
print(strength(longest_bridge))
