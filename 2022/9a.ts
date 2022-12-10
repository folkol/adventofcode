import * as fs from "fs";
import {strict as assert} from "assert";

type Pos = [number, number]

let directions: Record<string, Pos> = {
    'R': [1, 0],
    'L': [-1, 0],
    'U': [0, 1],
    'D': [0, -1],
}

let distance = (H: Pos, T: Pos) => Math.max(Math.abs(H[0] - T[0]), Math.abs(H[1] - T[1]));

function move(H: Pos, T: Pos, step: Pos): [Pos, Pos] {
    let hNext: Pos = [H[0] + step[0], H[1] + step[1]];
    let tNext = distance(hNext, T) > 1 ? H : T
    return [hNext, tNext]
}

let steps: Pos[] = fs.readFileSync('9.dat', 'utf-8')
    .split('\n')
    .map(line => line.split(' '))
    .flatMap(([a, b]) => Array(Number(b)).fill(directions[a]));

let [H, T]: [Pos, Pos] = [[0, 0], [0, 0]];
let visited = new Set<string>([T.toString()]);
steps.forEach((step) => {
    [H, T] = move(H, T, step);
    visited.add(T.toString());
})
console.log(visited.size)
assert(visited.size === 5858)