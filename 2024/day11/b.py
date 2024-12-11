from functools import cache

with open('input.dat') as f:
    initial_arrangement = [int(x) for x in f.read().split()]


@cache
def apply_rule_rec(number, blinks):
    if blinks == 0:
        return 1
    elif number == 0:
        return apply_rule_rec(1, blinks - 1)
    elif len(str(number)) % 2 == 0:
        str_as_num = str(number)
        left, right = str_as_num[:len(str_as_num) // 2], str_as_num[len(str_as_num) // 2:]
        return apply_rule_rec(int(left), blinks - 1) + apply_rule_rec(int(right), blinks - 1)
    else:
        return apply_rule_rec(number * 2024, blinks - 1)


print(sum(apply_rule_rec(n, 75) for n in initial_arrangement))
