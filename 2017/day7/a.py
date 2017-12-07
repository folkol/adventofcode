"""Prints data in a form suitable for tsort.

    usage: python3 a.py <programs.dat | tsort | head -1
"""
import re
from sys import stdin

for line in stdin:
    name, weight, *children = re.findall('\w+', line)
    for child in children or [name]:
        print(name, child)
