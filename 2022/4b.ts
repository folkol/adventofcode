import * as fs from "fs";
import {strict as assert} from 'node:assert';

let overlappingPairs = 0;
let data = fs.readFileSync('4.dat', 'utf-8');
data.trimEnd().split('\n').forEach(line => {
    let [aLo, aHi, bLo, bHi] = line.split(/[-,]/).map(Number)
    if (aHi >= bLo && aLo <= bHi) {
        overlappingPairs++;
    }
})
console.log(overlappingPairs)
assert(overlappingPairs === 815)
