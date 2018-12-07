import re
from collections import defaultdict

steps = set()
dependencies = defaultdict(set)
with open('steps.dat') as f:
    for line in f:
        match = re.match('Step (.) must be finished before step (.) can begin.', line)
        dependency, step = match.groups()
        steps.add(dependency)
        steps.add(step)
        dependencies[step].add(dependency)

order = []
while len(order) < len(steps):
    candidates = {step for step in steps if step not in order and dependencies[step] <= set(order)}
    next_step = sorted(candidates)[0]
    order.append(next_step)
print(''.join(order))
