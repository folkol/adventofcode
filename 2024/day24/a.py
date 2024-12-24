import re

GATE_PATTERN = r'(.*) (AND|OR|XOR) (.*) -> (.*)'

with open('input.dat') as f:
    fst, snd = f.read().split('\n\n')
    inputs = {k: int(v) for line in fst.splitlines() for k, v in [line.split(': ')]}
    gates = {
        output: parts
        for line in snd.splitlines()
        for *parts, output in [re.match(GATE_PATTERN, line).groups()]
    }


def resolve(gate):
    if gate in inputs:
        return inputs[gate]
    match gates[gate]:
        case a, 'AND', b:
            return resolve(a) & resolve(b)
        case a, 'OR', b:
            return resolve(a) | resolve(b)
        case a, 'XOR', b:
            return resolve(a) ^ resolve(b)


outputs = sorted((g for g in gates if g.startswith('z')), reverse=True)
bits = (str(resolve(output)) for output in outputs)
print(int(''.join(bits), 2))
