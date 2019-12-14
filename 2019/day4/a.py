from itertools import product

def good_candidate(candidate):
    digits = str(candidate)
    for i in range(len(digits) - 1):
        if digits[i + 1] < digits[i]:
            return False
    repeated_digit = False
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            repeated_digit = True
    if not repeated_digit:
        return False
    return True


num_matching = sum(1 for candidate in range(382345, 843167 + 1) if good_candidate(candidate))
print(num_matching)
