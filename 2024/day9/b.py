with open('input.dat') as f:
    data = f.read()
    file_sizes = {}
    disk_map = []
    for i, e in enumerate(data):
        size = int(e)
        if i % 2 == 0:
            file_id = int(i) // 2
            disk_map.extend([file_id] * size)
            file_sizes[file_id] = size
        else:
            disk_map.extend(['.'] * size)


def find_empty_space(width):
    for i in range(len(disk_map) - width):
        if disk_map[i:i + width] == ['.'] * width:
            return i
    return -1


max_file_id = len(data) // 2
for file_id in reversed(range(max_file_id + 1)):
    file_pos = disk_map.index(file_id)
    empty_start = find_empty_space(file_sizes[file_id])
    if empty_start != -1 and empty_start < file_pos:
        disk_map[empty_start:empty_start + file_sizes[file_id]] = [file_id] * file_sizes[file_id]
        disk_map[file_pos:file_pos + file_sizes[file_id]] = ['.'] * file_sizes[file_id]
        continue

print(sum(int(i) * int(j) if j != '.' else 0 for i, j in enumerate(disk_map)))
