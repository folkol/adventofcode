from collections import defaultdict, deque

program = [x.split() for x in open('program.dat')]


class Thread(object):
    def __init__(self, pid):
        self.pc = 0
        self.pid = pid
        self.messages = deque()
        self.registers = defaultdict(int)
        self.registers['p'] = self.pid
        self.blocked = False
        self.num_sent = 0

    def get(self, reg):
        try:
            val = int(reg)
        except ValueError:
            val = self.registers[reg]
        return val


def op_set(thread, reg, value):
    thread.registers[reg] = thread.get(value)


def op_add(thread, reg, value):
    thread.registers[reg] += thread.get(value)


def op_mul(thread, reg, value):
    val = thread.get(value)
    thread.registers[reg] *= val


def op_mod(thread, reg, value):
    thread.registers[reg] %= thread.get(value)


def op_snd(thread, reg, target):
    target.messages.append(thread.registers[reg])
    thread.num_sent += 1


ops = {
    'set': op_set,
    'add': op_add,
    'mul': op_mul,
    'mod': op_mod,
    'snd': op_snd
}

thread0 = Thread(0)
thread1 = Thread(1)

threads = [thread0, thread1]
while any(not thread.blocked for thread in threads):
    for thread in threads:
        if thread.pc < 0 or thread.pc >= len(program):
            print(thread.pid, 'blocked')
            thread.blocked = True
            continue

        thread.blocked = False
        op, reg, *args = program[thread.pc]

        if op == 'jgz':
            x = thread.get(reg)
            if x > 0:
                try:
                    thread.pc += int(args[0])
                    continue
                except ValueError:
                    thread.pc += thread.registers[args[0]]
                    continue
        elif op == 'snd':
            other = threads[thread.pid - 1]
            op_snd(thread, reg, other)
        elif op == 'rcv':
            if not thread.messages:
                thread.blocked = True
                continue

            thread.registers[reg] = thread.messages.popleft()
        else:
            ops[op](thread, reg, *args)

        thread.pc += 1

assert thread1.num_sent == 8001, thread1
print(thread1.num_sent)
