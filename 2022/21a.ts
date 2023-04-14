import * as fs from "fs";
import * as assert from "assert";


interface Monkey {
    name: string,
    value?: number,
    operand?: (a: number, b: number) => number,
    operands?: string[];
}

function parseMonkey(line: string): Monkey {
    let [name, expression] = line.split(': ');
    let value = Number(expression);
    if (Number.isInteger(value)) {
        return {
            name,
            value: value,
            operand: () => value,
            operands: []
        }
    } else {
        let [a, op, b] = expression.split(' ');
        let operand;
        if (op === '+') {
            operand = (a, b) => a + b;
        } else if (op === '-') {
            operand = (a, b) => a - b;
        } else if (op === '*') {
            operand = (a, b) => a * b;
        } else {
            operand = (a, b) => a / b;
        }
        return {
            name,
            operand,
            operands: [a, b]
        };
    }
}

let monkeys = fs.readFileSync('21.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(parseMonkey);

function monkeySort(monkeys: Monkey[], currentMonkey: string = 'root', orderedMonkeys: Monkey[] = []) {
    let node = monkeys.find(monkey => monkey.name === currentMonkey);
    orderedMonkeys.push(node)
    for (let subMonkey of node?.operands) {
        monkeySort(monkeys, subMonkey, orderedMonkeys);
    }
    return orderedMonkeys
}

let orderedMonkeys = monkeySort(monkeys.map(monkey => ({
    name: monkey.name,
    operand: monkey.operand,
    operands: monkey.operands.slice(),
    value: monkey.value
})), 'root')

for (let monkey of orderedMonkeys.reverse()) {
    monkey.value = monkey.operand(
        orderedMonkeys.find(m => m.name === monkey.operands[0])?.value,
        orderedMonkeys.find(m => m.name === monkey.operands[1])?.value
    )
}

// let ans = values.get('root');
let ans = orderedMonkeys.find(m => m.name === 'root').value;
console.log(ans)
assert(ans === 331319379445180)