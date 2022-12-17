import * as fs from 'node:fs';
import * as assert from "assert";

let sensors = fs.readFileSync('15.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(line => line.matchAll(/-?\d+/g))
    .map(matches => [...matches].map(Number))
    .map(([sx, sy, bx, by]) => [sx, sy, Math.abs(sx - bx) + Math.abs(sy - by)]);

function foundDistressBeacon(x, y) {
    if (x < 0 || x > 4000000 || y < 0 || y > 4000000) {
        return false
    }
    for (let [sensorX, sensorY, sensorRange] of sensors) {
        let distance = Math.abs(sensorX - x) + Math.abs(sensorY - y);
        if (distance <= sensorRange) {
            return false
        }
    }
    return true
}

function* tracePerimeters(sensors) {
    for (let [sensorX, sensorY, sensorRange] of sensors) {
        let [probeX, probeY] = [sensorX - sensorRange - 1, sensorY]
        for (let [dx, dy] of [[1, -1], [1, 1], [-1, 1], [-1, -1]]) {
            for (let i = 0; i < sensorRange + 2; i++, probeX += dx, probeY += dy) {
                yield [probeX, probeY]
            }
        }
    }
}

let ans = 0;
for (let [x, y] of tracePerimeters(sensors)) {
    if (foundDistressBeacon(x, y)) {
        ans = x * 4000000 + y;
        break;
    }
}
console.log(ans)
assert(ans === 13340867187704)