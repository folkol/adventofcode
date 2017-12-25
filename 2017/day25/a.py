from collections import namedtuple

State = namedtuple('State', ['next_state', 'output', 'move'])
LEFT = -1
RIGHT = 1

state = 'A'
states = {
    'A': {0: State('B', 1, RIGHT), 1: State('E', 1, LEFT)},
    'B': {0: State('C', 1, RIGHT), 1: State('F', 1, RIGHT)},
    'C': {0: State('D', 1, LEFT), 1: State('B', 0, RIGHT)},
    'D': {0: State('E', 1, RIGHT), 1: State('C', 0, LEFT)},
    'E': {0: State('A', 1, LEFT), 1: State('D', 0, RIGHT)},
    'F': {0: State('A', 1, RIGHT), 1: State('C', 1, RIGHT)}
}

tape = {}
pos = 0
for _ in range(12523873):
    val = tape.get(pos, 0)
    current_state = states[state][val]
    tape[pos] = current_state.output
    pos += current_state.move
    state = current_state.next_state

print(sum(tape.values()))
