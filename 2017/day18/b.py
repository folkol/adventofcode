from collections import defaultdict, deque

program = [x.split() for x in """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d""".split('\n')]
program = [x.split() for x in open('program.dat')]
LATEST_SOUND = 'LATEST_SOUND'


def op_set(registers, reg, value):
    try:
        registers[reg] = int(value)
    except ValueError:
        registers[reg] = registers[value]


def op_add(registers, reg, value):
    try:
        registers[reg] += int(value)
    except ValueError:
        registers[reg] += registers[value]


def op_mul(registers, reg, value):
    try:
        registers[reg] *= int(value)
    except ValueError:
        registers[reg] *= registers[value]


def op_mod(registers, reg, value):
    try:
        registers[reg] %= int(value)
    except ValueError:
        registers[reg] %= registers[value]


def op_snd(thread, reg, target):
    target['messages'].append(thread['registers'][reg])
    thread['num_sent'] += 1


ops = {
    'set': op_set,
    'add': op_add,
    'mul': op_mul,
    'mod': op_mod,
    'snd': op_snd
}

thread0 = {
    'pc': 0,
    'pid': 0,
    'messages': deque(),
    'registers': defaultdict(int),
    'blocked': False,
    'num_sent': 0
}
thread0['registers']['p'] = 0

thread1 = {
    'pc': 0,
    'pid': 1,
    'registers': defaultdict(int),
    'messages': deque(),
    'blocked': False,
    'num_sent': 0
}
thread1['registers']['p'] = 1

threads = [thread0, thread1]
while any(not thread['blocked'] for thread in threads):
    assert thread0['registers'] is not thread1['registers']
    for thread in threads:
        assert 0 <= thread['pc']
        assert thread['pc'] < len(program)
        for register, value in thread['registers'].items():
            assert isinstance(value, int)

        if thread['pc'] < 0 or thread['pc'] >= len(program):
            print(thread['pid'], 'blocked')
            thread['blocked'] = True
            continue

        thread['blocked'] = False
        op, reg, *args = program[thread['pc']]

        if op == 'jgz':
            try:
                x = int(reg)
            except ValueError:
                x = thread['registers'][reg]
            if x > 0:
                try:
                    thread['pc'] += int(args[0])
                    continue
                except ValueError:
                    thread['pc'] += thread['registers'][args[0]]
                    continue
        elif op == 'snd':
            # print(thread['pid'])
            other = threads[thread['pid'] - 1]
            assert other is not thread
            op_snd(thread, reg, other)
        elif op == 'rcv':
            if not thread['messages']:
                thread['blocked'] = True
                continue

            thread['registers'][reg] = thread['messages'].popleft()
        else:
            ops[op](thread['registers'], reg, *args)

        thread['pc'] += 1

print(thread0)
print(thread1)
print(thread1['num_sent'])
