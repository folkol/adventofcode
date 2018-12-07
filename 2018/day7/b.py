import re
from collections import defaultdict
from heapq import heappush, heappop
from itertools import count

counter = count()
steps = set()
dependencies = defaultdict(set)
with open('steps.dat') as f:
    for line in f:
        match = re.match('Step (.) must be finished before step (.) can begin.', line)
        dependency, step = match.groups()
        steps.update(dependency, step)
        dependencies[step].add(dependency)

order = []
workers = {worker: '.' for worker in range(1, 6)}
time = 0
queue = []
enqueued = []

for time in count():
    while queue and queue[0][0] <= time:
        worker, task = heappop(queue)[2]
        workers[worker] = '.'
        order.append(task)
    if len(order) == len(steps):
        break
    candidates = {s for s in steps if s not in enqueued and dependencies[s] <= set(order)}
    idle_workers = {worker for worker, task in workers.items() if task == '.'}
    for candidate, worker in zip(sorted(candidates), idle_workers):
        enqueued.append(candidate)
        workers[worker] = candidate
        heappush(queue, (time + ord(candidate) - 4, next(counter), (worker, candidate)))
    print(time, *workers.values(), ''.join(order), sep='\t')

print(f'Assembly done in {time} seconds!')
