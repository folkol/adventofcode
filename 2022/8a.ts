import * as fs from "fs";
import {strict as assert} from "assert";

let heights = fs.readFileSync('8.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(line => line.split('').map(Number));

function isVisible(row: number, col: number) {
    function isVisibleFrom(y: number, x: number, dy: number, dx: number): boolean {
        if (y === row && x === col) {
            return true;
        }
        if (heights[y][x] >= heights[row][col]) {
            return false;
        }
        return isVisibleFrom(y + dy, x + dx, dy, dx);
    }

    return isVisibleFrom(row, 0, 0, +1)
        || isVisibleFrom(row, heights[row].length - 1, 0, -1)
        || isVisibleFrom(0, col, +1, 0)
        || isVisibleFrom(heights.length - 1, col, -1, 0);
}

let ans = 0;
for (let row = 0; row < heights.length; row++) {
    for (let col = 0; col < heights[row].length; col++) {
        if (isVisible(row, col)) {
            ans++;
        }
    }
}
console.log(ans);
assert(ans === 1849)
