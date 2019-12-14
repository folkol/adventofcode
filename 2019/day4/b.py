from itertools import product
from collections import Counter

def good_candidate(candidate):
    digits = str(candidate)
    for i in range(len(digits) - 1):
        if digits[i + 1] < digits[i]:
            return False
    repeated_digits = []
    for i in range(len(digits) - 1):
        if digits[i] == digits[i + 1]:
            repeated_digits.append(digits[i])
    repeated_digits = [digit for digit in repeated_digits if digit * 3 not in digits]
    if not repeated_digits:
        return False
    return True


num_matching = sum(1 for candidate in range(382345, 843167 + 1) if good_candidate(candidate))
print(num_matching)
