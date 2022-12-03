import * as fs from 'fs';
import {strict as assert} from 'node:assert';

function priority(item: string) {
    if (item.toLowerCase() === item) {
        return 1 + item.charCodeAt(0) - 'a'.charCodeAt(0);
    } else {
        return 27 + item.charCodeAt(0) - 'A'.charCodeAt(0);
    }
}

let prioritySum = 0;
let rucksacks = fs.readFileSync('3.dat', 'utf-8').trimEnd().split('\n');
while (rucksacks.length) {
    let group = rucksacks.splice(-3)
    let seenTypes: Record<string, number> = {};
    for (let rucksack of group) {
        let uniqueTypes = new Set(rucksack);
        for (let type of uniqueTypes) {
            let peersWithType = seenTypes[type] || 0;
            if (peersWithType === 2) {
                prioritySum += priority(type);
            }
            seenTypes[type] = peersWithType + 1;
        }
    }
}

console.log(prioritySum);
assert(prioritySum === 2864)
