from collections import deque

with open('input.dat') as f:
    garden = {
        x + y * 1j: plant
        for y, line in enumerate(f)
        for x, plant in enumerate(line.rstrip())
    }


def extract_region(z, plant):
    region, queue, seen = {z}, deque([z]), set()
    while queue:
        cur = queue.popleft()
        garden[cur] = ''
        region.add(cur)
        for d in [1, -1, 1j, -1j]:
            neighbor = cur + d
            if garden.get(neighbor) == plant and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)

    return region


def calculate_cost(plot):
    region = extract_region(plot, garden[plot])
    area = len(region)
    perimeter = sum(
        1
        for z in region
        for n in [1, -1, 1j, -1j]
        if z + n not in region
    )
    return area * perimeter


print(sum(calculate_cost(plot) for plot, plant in garden.items() if plant))
