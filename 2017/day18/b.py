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

    def get(self, value):
        try:
            return int(value)
        except ValueError:
            return self.registers[value]

    def op_set(self, reg, value):
        self.registers[reg] = self.get(value)

    def op_add(self, reg, value):
        self.registers[reg] += self.get(value)

    def op_mul(self, reg, value):
        self.registers[reg] *= self.get(value)

    def op_mod(self, reg, value):
        self.registers[reg] %= self.get(value)

    def op_snd(self, reg, target):
        target.messages.append(self.registers[reg])
        self.num_sent += 1


ops = {
    'set': Thread.op_set,
    'add': Thread.op_add,
    'mul': Thread.op_mul,
    'mod': Thread.op_mod,
    'snd': Thread.op_snd
}

threads = [Thread(0), Thread(1)]
while not all(t.blocked for t in threads):
    for thread in threads:
        if not 0 <= thread.pc < len(program):
            thread.blocked = True
            continue

        op, *args = program[thread.pc]

        if op == 'jgz':
            if thread.get(args[0]) > 0:
                thread.pc += thread.get(args[1])
                continue
        elif op == 'snd':
            other = threads[thread.pid - 1]
            thread.op_snd(args[0], other)
        elif op == 'rcv':
            if not thread.messages:
                thread.blocked = True
                continue

            thread.blocked = False
            thread.registers[args[0]] = thread.messages.popleft()
        else:
            ops[op](thread, *args)

        thread.pc += 1

t = threads[1]
assert t.num_sent == 8001, t
print(t.num_sent)
