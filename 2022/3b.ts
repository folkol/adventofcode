import * as fs from 'fs';
import {strict as assert} from 'node:assert';

function priority(item: string) {
    if (item.toLowerCase() === item) {
        return 1 + item.charCodeAt(0) - 'a'.charCodeAt(0);
    } else {
        return 27 + item.charCodeAt(0) - 'A'.charCodeAt(0);
    }
}

function* groups(items: string[]) {
    let group: string[] = [];
    for (let item of items) {
        group.push(item);
        if (group.length === 3) {
            yield group
            group = []
        }
    }
    if (group.length > 0) {
        yield group;
    }
}

let data = fs.readFileSync('3.dat', 'utf-8');
let prioritySum = 0;
for (let group of groups(data.split('\n'))) {
    let typeCounts: Record<string, number> = {};
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
