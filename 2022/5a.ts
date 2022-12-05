import * as fs from "fs";
import {strict as assert} from "node:assert"

let stacks: string[][] = [[], [], [], [], [], [], [], [], []]
let lines = fs.readFileSync('5.dat', 'utf-8').trimEnd().split('\n');
lines.forEach(line => {
    if (line.startsWith('move')) {
        let [n, from, to] = line.match(/\d+/g)?.map(Number) as number[];
        let crates = stacks[from - 1].splice(-Number(n));
        stacks[to - 1].push(...crates.reverse());
    } else {
        for (let i = 0, stack = 0; i < line.length; stack += 1, i = stack * 4) {
            if (line[i] === '[') {
                stacks[stack].unshift(line[i + 1])
            }
        }
    }
})
let ans = stacks.map(stack => stack.slice(-1)).join('')
console.log(ans)
assert(ans === 'SVFDLGLWV')
