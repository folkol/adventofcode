"""Solves an inverse captcha á la [http://adventofcode.com/2017/day/1]."""
import sys

captcha = sys.stdin.read()
digits = [int(digit) for digit in captcha]


def successor(xs, i):
    """Returns xs[i + 1], wraps around if necessary."""
    return xs[(i + 1) % len(xs)]


print(sum(int(e) for i, e in enumerate(digits) if e == successor(digits, i)))
