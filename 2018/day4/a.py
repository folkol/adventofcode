import re
from collections import defaultdict, Counter
from datetime import datetime, timedelta


def date_range(begin, end):
    while begin < end:
        yield begin
        begin += timedelta(minutes=1)


with open('data.dat') as f:
    data = sorted(f.readlines())

guards = defaultdict(list)

fell_asleep = guard = None
for line in data:
    date = datetime.strptime(line[1:17], '%Y-%m-%d %H:%M')
    match = re.match('.*Guard #(\d+) begins shift', line)
    if match:
        guard = match.group(1)
    if 'falls asleep' in line:
        fell_asleep = date
    if 'wakes up' in line:
        for d in date_range(fell_asleep, date):
            guards[guard].append(d.minute)

guard, minutes = max(guards.items(), key=lambda x: len(x[1]))
minute, count = Counter(minutes).most_common(1)[0]

print(int(guard) * int(minute))
