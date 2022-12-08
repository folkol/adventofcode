import * as fs from "fs";
import {strict as assert} from 'node:assert'

let heights = fs.readFileSync('8.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(line => line.split('').map(Number));

function scenicScore(row: number, col: number) {
    function look(y: number, x: number, dy: number, dx: number): number {
        if (y <= 0 || y >= heights.length - 1 || x <= 0 || x >= heights[y].length - 1) {
            return 0
        }
        if (heights[y + dy][x + dx] >= heights[row][col]) {
            return 1
        }
        return 1 + look(y + dy, x + dx, dy, dx);
    }

    return look(row, col, -1, 0)
        * look(row, col, +1, 0)
        * look(row, col, 0, -1)
        * look(row, col, 0, +1)
}

let ans = 0;
for (let row = 0; row < heights.length; row++) {
    for (let col = 0; col < heights[row].length; col++) {
        ans = Math.max(ans, scenicScore(row, col))
    }
}
console.log(ans);
assert(ans === 201600)
