import * as fs from 'fs';
import {strict as assert} from 'node:assert';

function priority(item: string) {
    if (item.toLowerCase() === item) {
        return 1 + item.charCodeAt(0) - 'a'.charCodeAt(0);
    } else {
        return 27 + item.charCodeAt(0) - 'A'.charCodeAt(0);
    }
}

let rucksacks = fs.readFileSync('3.dat', 'utf-8').split('\n');
let prioritySum = 0;
while (rucksacks.length) {
    let typeCounts: Record<string, number> = {};
    let group = rucksacks.splice(-3);
    for (let rucksack of group) {
        for (let type of new Set(rucksack)) {
            let typeCount = typeCounts[type] || 0;
            if (typeCount === 2) {
                prioritySum += priority(type);
            }
            typeCounts[type] = typeCount + 1;
        }
    }
}

console.log(prioritySum);
assert(prioritySum === 2864)
