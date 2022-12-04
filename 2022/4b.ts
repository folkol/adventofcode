import * as fs from "fs";
import {strict as assert} from 'node:assert';

function overlap(a: string, b: string) {
    let [aLo, aHi] = a.split('-').map(Number);
    let [bLo, bHi] = b.split('-').map(Number);
    return aHi >= bLo && aLo <= bHi
}

let overlappingPairs = 0;
let data = fs.readFileSync('4.dat', 'utf-8');
data.trimEnd().split('\n').forEach(line => {
    let [a, b] = line.split(',');
    if (overlap(a, b)) {
        overlappingPairs++;
    }
})
console.log(overlappingPairs)
assert(overlappingPairs === 815)
