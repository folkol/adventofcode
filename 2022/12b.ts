import * as fs from "fs";
import {strict as assert} from "assert";

let start = {x: 0, y: 0};
let heights = fs.readFileSync('12.dat', 'utf-8')
    .split('\n')
    .map((line, row) => line.split('').map((c, col) => {
        if (c === 'S') {
            return 0
        } else if (c === 'E') {
            [start.x, start.y] = [row, col];
            return 'z'.charCodeAt(0) - 'a'.charCodeAt(0)
        }
        return c.charCodeAt(0) - 'a'.charCodeAt(0);
    }));

let distances = heights.map(row => row.map(() => Infinity));
distances[start.x][start.y] = 0;
let ans = Infinity;
for (let todo = heights.flatMap((row, i) => row.map((_, j) => [i, j])); todo.length;) {
    todo.sort(([x1, y1], [x2, y2]) => distances[x1][y1] - distances[x2][y2]);
    let [x, y] = todo.shift()!;
    if (heights[x][y] === 0) {
        ans = distances[x][y];
        break;
    }
    for (let [dx, dy] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
        let [i, j] = [x + dx, y + dy];
        if (heights[x]?.[y] <= heights[i]?.[j] + 1) {
            distances[i][j] = Math.min(distances[i][j], distances[x][y] + 1);
        }
    }
}
console.log(ans);
assert(ans === 512);
