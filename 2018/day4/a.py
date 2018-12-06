import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta


def date_range(first, last):
    while first < last:
        yield first
        first += timedelta(minutes=1)


def sleepyness(item):
    """Returns the number of minutes a guard spent sleeping on duty."""
    _, minutes = item
    return len(minutes)


with open('data.dat') as f:
    data = sorted(f.readlines())

guards = defaultdict(list)
guard = fell_asleep = None
for line in data:
    date = datetime.strptime(line[1:17], '%Y-%m-%d %H:%M')
    match = re.match('.*Guard #(\d+) begins shift', line)
    if match:
        guard = int(match.group(1))
    if 'falls asleep' in line:
        fell_asleep = date
    if 'wakes up' in line:
        for d in date_range(fell_asleep, date):
            guards[guard].append(d.minute)

guard, minutes = max(guards.items(), key=sleepyness)
minute = Counter(minutes).most_common(1)[0][0]
print(guard * minute)
