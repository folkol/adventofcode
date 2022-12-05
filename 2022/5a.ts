import * as fs from "fs";
import {strict as assert} from "node:assert"

let stacks: string[][] = [[], [], [], [], [], [], [], [], []]
let lines = fs.readFileSync('5.dat', 'utf-8').trimEnd().split('\n');
lines.forEach(line => {
    if (line.startsWith('move')) {
        let [n, from, to] = line.match(/\d+/g)?.map(Number) as number[];
        stacks[to - 1].push(...stacks[from - 1].splice(-Number(n)).reverse());
    } else {
        for (let i = 0; i * 4 < line.length; i++) {
            if (line[i * 4] === '[') {
                stacks[i].unshift(line[i * 4 + 1])
            }
        }
    }
})
let ans = stacks.map(stack => stack.slice(-1)).join('')
console.log(ans)
assert(ans === 'SVFDLGLWV')
