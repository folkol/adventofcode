import * as fs from "fs";
import {strict as assert} from "node:assert"

let stacks: Record<string, string[]> = {}
let lines = fs.readFileSync('4.dat', 'utf-8').trimEnd().split('\n');
lines.forEach(line => {
    if (line.startsWith('move')) {
        let [n, from, to] = line.match(/\d+/g) as string[];
        stacks[to].push(...stacks[from].splice(-Number(n)))
    } else {
        let crates = line.matchAll(/[A-Z]/g);
        for (let crate of crates) {
            let stack = 1 + (crate.index as number - 1) / 4;
            stacks[stack] = stacks[stack] || []
            stacks[stack].unshift(crate[0])
        }
    }
})
let ans = Object.entries(stacks).sort().map(entry => {
    return entry[1].slice(-1)
}).join('')
console.log(ans)
assert(ans === 'DCVTCVPCL')
