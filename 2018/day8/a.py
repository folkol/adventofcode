with open('tree.dat') as f:
    numbers = iter(f.read().split())

sum = 0


def read_node(numbers):
    global sum
    children = []
    metadata_entries = []
    num_children = next(numbers)
    num_metadata_entries = next(numbers)
    for _ in range(int(num_children)):
        read_node(numbers)
    for _ in range(int(num_metadata_entries)):
        sum += int(next(numbers))
    return {
        'children': children,
        'metadata_entries': metadata_entries
    }


read_node(numbers)

print(sum)
