with open('input.dat') as f:
    initial_arrangement = [int(x) for x in f.read().split()]


def apply_rules(x):
    if x == 0:
        return [1]
    elif len(str(x)) % 2 == 0:
        str_as_num = str(x)
        left, right = str_as_num[:len(str_as_num) // 2], str_as_num[len(str_as_num) // 2:]
        return [int(left), int(right)]
    else:
        return [x * 2024]


numbers = initial_arrangement
for blink in range(25):
    numbers = [number for number in numbers for number in apply_rules(number)]

print(len(numbers))
