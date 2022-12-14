import * as fs from "fs";
import {strict as assert} from "assert";

let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
let paths: number[][][] = fs.readFileSync('14.dat', 'utf-8')
    .split('\n')
    .map(line => line.split(' -> ').map(word => {
        let [x, y] = word.split(',').map(Number);
        minX = Math.min(x, minX)
        minY = Math.min(y, minY)
        maxX = Math.max(x, maxX)
        maxY = Math.max(y, maxY)
        return [x, y]
    }));

maxY = 2 + maxY;
minX = 500 - maxY * 2;
maxX = 500 + maxY * 2
paths.push([[0, maxY], [maxX, maxY]]);

let [width, height] = [maxX - minX + 1, maxY + 1];
let cave = []
for (let i = 0; i < height; i++) {
    cave.push(new Array(width).fill(0))
}

paths.forEach(path => path.reduce((prev, cur) => {
    let [xFrom, yFrom] = prev, [xTo, yTo] = cur;
    if (xFrom > xTo) {
        [xFrom, xTo] = [xTo, xFrom]
    }
    if (yFrom > yTo) {
        [yFrom, yTo] = [yTo, yFrom]
    }
    for (let y = yFrom; y <= yTo; y++) {
        for (let x = xFrom; x <= xTo; x++) {
            cave[y][x - minX] = 1
        }
    }
    return cur;
}));

function occupied(x: number, y: number): boolean {
    return cave[y]?.[x] || 0
}

let done = false;
let ans = 0
while (!done) {
    let [x, y] = [500 - minX, 0];  // find '+'
    let [xStart, yStart] = [x, y];
    while (true) {
        if (!occupied(x, y + 1)) {
            [x, y] = [x, y + 1]
        } else if (!occupied(x - 1, y + 1)) {
            [x, y] = [x - 1, y + 1]
        } else if (!occupied(x + 1, y + 1)) {
            [x, y] = [x + 1, y + 1]
        } else {
            cave[y][x] = 2
            ans++
            if (x === xStart && y === yStart) {
                done = true;
            }
            break;
        }
    }
}
console.log(ans)
assert(ans === 25500)