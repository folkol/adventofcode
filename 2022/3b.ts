import * as fs from 'fs';
import {strict as assert} from 'node:assert';

function priority(item: string) {
    return 'øabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'.indexOf(item[0]);
}

function intersect(a: string, b: string): string {
    return [...a].filter(e => b.includes(e)).join('')
}

let prioritySum = 0;
let rucksacks = fs.readFileSync('3.dat', 'utf-8').trimEnd().split('\n');
while (rucksacks.length) {
    let group = rucksacks.splice(-3)
    let commonItem = group.reduce(intersect);
    prioritySum += priority(commonItem);
}
console.log(prioritySum);
assert(prioritySum === 2864)
