import * as fs from "fs";
import {strict as assert} from "assert";

function parseNumbers(line: string) {
    return [...line.matchAll(/\d+/g)].map(Number);
}

function parseOp(line: string) {
    let [op, arg] = line.split(' ').slice(-2)
    if (arg === 'old') {
        return (x: number): number => x ** 2;
    } else if (op === '+') {
        return (x: number): number => x + Number(arg);
    } else {
        return (x: number): number => x * Number(arg);
    }
}

function parseMonkey(chunk: string[]) {
    return {
        items: parseNumbers(chunk[1]),
        operation: parseOp(chunk[2]),
        divisor: parseNumbers(chunk[3])[0],
        happy: parseNumbers(chunk[4])[0],
        sad: parseNumbers(chunk[5])[0],
        activity: 0,
    };
}

let chunks: string[][] = [[]]
fs.readFileSync('11.dat', 'utf-8')
    .split('\n')
    .forEach(line => line ? chunks[chunks.length - 1].push(line) : chunks.push([]));

let monkeys = chunks.map(parseMonkey);
for (let round = 0; round < 20; round++) {
    for (let monkey of monkeys) {
        for (let item of monkey.items.splice(0)) {
            monkey.activity++
            item = Math.floor(monkey.operation(item) / 3);
            monkeys[item % monkey.divisor ? monkey.sad : monkey.happy].items.push(item);
        }
    }
}
monkeys.sort((a, b) => b.activity - a.activity)
let monkeyBusiness = monkeys[0].activity * monkeys[1].activity
console.log(monkeyBusiness)
assert(monkeyBusiness === 112815)