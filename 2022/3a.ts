import * as fs from 'fs';
import {strict as assert} from 'node:assert';

function priority(item: string) {
    if (item.toLowerCase() === item) {
        return 1 + item.charCodeAt(0) - 'a'.charCodeAt(0);
    } else {
        return 27 + item.charCodeAt(0) - 'A'.charCodeAt(0);
    }
}

let data = fs.readFileSync('3.dat', 'utf-8');
let prioritySum = 0;
data.split('\n').forEach(line => {
    let compartments: Record<string, number> = {};
    let compartmentSize = line.length / 2;
    Array.prototype.forEach.call(line, (item, index) => {
        let currentCompartment = Number(index < compartmentSize);
        let previousCompartment = compartments[item] ?? currentCompartment;
        if (previousCompartment !== currentCompartment) {
            prioritySum += priority(item);
        }
        compartments[item] = currentCompartment;
    })
})
console.log(prioritySum);
assert(prioritySum === 8202)
