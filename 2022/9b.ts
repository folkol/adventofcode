import * as fs from "fs";
import {strict as assert} from "assert";

let directions: Record<string, number[]> = {
    'R': [1, 0],
    'L': [-1, 0],
    'U': [0, 1],
    'D': [0, -1],
}

function add(s: number[], ds: number[]) {
    s[0] += ds[0];
    s[1] += ds[1]
}

let steps: number[][] = fs.readFileSync('9.dat', 'utf-8')
    .split('\n')
    .map(line => line.split(' '))
    .flatMap(([a, b]) => Array(Number(b)).fill(directions[a]));

let segments: number[][] = [];
for (let i = 0; i < 10; i++) {
    segments.push([0, 0])
}
let visited = new Set<string>([segments.slice(-1).toString()]);
for (let step of steps) {
    add(segments[0], step)
    segments.slice(1).forEach((segment, i) => {
        let H = segments[i];
        let [dy, dx] = [H[0] - segment[0], H[1] - segment[1]];
        if (Math.abs(dy) > 1 || Math.abs(dx) > 1) {
            add(segment, [Math.sign(dy), Math.sign(dx)]);
        }
    })
    visited.add(segments.slice(-1).toString());
}
console.log(visited.size)
assert(visited.size === 2602)