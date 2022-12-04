import * as fs from "fs";
import {strict as assert} from "node:assert"

function subset(a: string, b: string) {
    let [aLo, aHi] = a.split('-').map(Number);
    let [bLo, bHi] = b.split('-').map(Number);
    return aLo <= bLo && aHi >= bHi
}

let overlappingPairs = 0;
let data = fs.readFileSync('4.dat', 'utf-8');
data.trimEnd().split('\n').forEach(line => {
    let [a, b] = line.split(',');
    if (subset(a, b) || subset(b, a)) {
        overlappingPairs++;
    }
})
console.log(overlappingPairs)
assert(overlappingPairs === 500)
