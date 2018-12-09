with open('tree.dat') as f:
    numbers = iter(f.read().split())


def read_node(numbers):
    global sum
    children = []
    metadata_entries = []
    num_children = int(next(numbers))
    num_metadata_entries = int(next(numbers))
    for _ in range(num_children):
        children.append(read_node(numbers))
    for _ in range(num_metadata_entries):
        metadata_entries.append(int(next(numbers)))
    value = 0
    if num_children == 0:
        value = sum(metadata_entries)
    else:
        for metadata_entry in metadata_entries:
            if metadata_entry == 0:
                continue
            if metadata_entry > len(children):
                continue
            value += children[metadata_entry - 1]['value']
    return {
        'children': children,
        'metadata_entries': metadata_entries,
        'value': value
    }


root = read_node(numbers)

print(root['value'])
