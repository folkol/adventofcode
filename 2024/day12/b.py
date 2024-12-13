from collections import deque

with open('input.dat') as f:
    original_garden = {
        x + y * 1j: plant
        for y, line in enumerate(f)
        for x, plant in enumerate(line.rstrip())
    }

garden = original_garden.copy()


def extract_region_and_perimeter(z, plant):
    region, queue, seen, perimeter = {z}, deque([z]), set(), set()
    while queue:
        cur = queue.popleft()
        garden[cur] = ''
        region.add(cur)
        for d in [1, -1, 1j, -1j]:
            neighbor = cur + d
            if original_garden.get(neighbor) == plant:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
            else:
                neighbor_ = (cur, d)
                perimeter.add(neighbor_)

    return region, perimeter


def trace_wall(perimeter, p):
    seen, queue = set(), deque([p])
    while queue:
        cur, normal = queue.popleft()
        seen.add((cur, normal))
        neighbors = [(cur + normal * 1j, normal), (cur - normal * 1j, normal)]
        queue.extend(n for n in neighbors if n not in seen and n in perimeter)
    return seen


def count_walls(perimeter):
    num_walls, seen = 0, set()
    for p in perimeter:
        if p not in seen:
            wall = trace_wall(perimeter, p)
            seen.update(wall)
            num_walls += 1
    return num_walls


def calculate_cost(plot):
    region, perimeter = extract_region_and_perimeter(plot, garden[plot])
    return len(region) * count_walls(perimeter)


print(sum(calculate_cost(plot) for plot, plant in garden.items() if plant))
