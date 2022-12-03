import * as fs from 'fs';
import {strict as assert} from 'node:assert';

function priority(item: string) {
    if (item.toLowerCase() === item) {
        return 1 + item.charCodeAt(0) - 'a'.charCodeAt(0);
    } else {
        return 27 + item.charCodeAt(0) - 'A'.charCodeAt(0);
    }
}

function intersect(a: Set<string>, b: Set<string>) {
    return new Set([...a].filter(e => b.has(e)));
}

let prioritySum = 0;
let rucksacks = fs.readFileSync('3.dat', 'utf-8').trimEnd().split('\n');
while (rucksacks.length) {
    let group = rucksacks.splice(-3)
    let [commonItem] = group.reduce((acc, x) => intersect(acc, new Set(x)), new Set(group[0]));
    prioritySum += priority(commonItem);
}

console.log(prioritySum);
assert(prioritySum === 2864)
