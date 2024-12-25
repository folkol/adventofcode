"""Generate dot graph for the given circuit.

$ pypy3 b.py | dot -Tpng -o circuit.png

The circuit is a https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder,
I couldn't come up with a way to solve this programmatically — so I printed the diagram
and manually inspected the circuit and fixed the crossed wires...
"""
import re

GATE_PATTERN = r'(.*) (AND|OR|XOR) (.*) -> (.*)'
GATE_COLORS = {'AND': "lightblue", 'OR': "green", 'XOR': "pink"}
GATE_SHAPES = {'AND': "diamond", 'OR': "hexagon", 'XOR': "triangle"}

with open('input.dat') as f:
    # with open('input_fixed.dat') as f:
    fst, snd = f.read().split('\n\n')

inputs = {k: int(v) for line in fst.splitlines() for k, v in [line.split(': ')]}
gates = {
    output: parts
    for line in snd.splitlines()
    for *parts, output in [re.match(GATE_PATTERN, line).groups()]
}

print('digraph {')
print('    node [style=filled];')
for n in inputs:
    color = 'green' if n.startswith('x') else 'lightblue'
    print(f'    "{n}" [color={color}];')

print('    {')
print('        rank=same;')
for g in [g for g in gates if g.startswith('z')]:
    print(f'        "{g}"')
print('    }')
for n in range(44):
    print(f'    "z{n + 1:02d}" -> "z{n:02d}" [style=invis];')

for a, op, b in gates.values():
    fillcolor = GATE_COLORS[op]
    shape = GATE_SHAPES[op]
    print(f'    "{a}_{op}_{b}" [label="{op}",shape={shape},fillcolor={fillcolor}];')

for g, (a, op, b) in gates.items():
    color = GATE_COLORS[op]
    print(f'    "{a}" -> "{a}_{op}_{b}";')
    print(f'    "{b}" -> "{a}_{op}_{b}";')
    print(f'    "{a}_{op}_{b}" -> "{g}" [color={color}];')

print('}')
