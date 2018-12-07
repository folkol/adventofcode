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

completed = []
workers = {worker: '.' for worker in range(1, 6)}
queue = []
enqueued = []

for time in count():
    while queue and queue[0][0] <= time:
        worker, task = heappop(queue)[2]
        workers[worker] = '.'
        completed.append(task)

    if len(completed) == len(steps):
        print(f'Assembly done in {time} seconds!')
        break

    candidates = {s for s in steps if s not in enqueued and dependencies[s] <= set(completed)}
    idle_workers = {worker for worker, task in workers.items() if task == '.'}
    for task, worker in zip(sorted(candidates), idle_workers):
        enqueued.append(task)
        workers[worker] = task
        duration = 60 + ord(task) - 64
        heappush(queue, (time + duration, next(counter), (worker, task)))
    print(time, *workers.values(), ''.join(completed), sep='\t')
