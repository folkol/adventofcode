import re
from collections import defaultdict

PATTERN = 'Step (.) must be finished before step (.) can begin'


def is_candidate(step):
    return step not in completed and dependencies[step].issubset(completed)


steps = set()
dependencies = defaultdict(set)

with open('steps.dat') as f:
    for line in f:
        dependency, step = re.match(PATTERN, line).groups()
        steps.update(dependency, step)
        dependencies[step].add(dependency)

completed = []
while len(completed) < len(steps):
    next_step = next(step for step in sorted(steps) if is_candidate(step))
    completed.append(next_step)

print(''.join(completed))
