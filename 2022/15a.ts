import * as fs from 'node:fs';
import * as assert from "assert";

function intersectLine([sensorX, sensorY, beaconX, beaconY]: number[]) {
    let distanceBeacon = Math.abs(beaconX - sensorX) + Math.abs(beaconY - sensorY);
    let distanceLine = Math.abs(sensorY - 2000000)
    return [sensorX - distanceBeacon + distanceLine, sensorX + distanceBeacon - distanceLine]
}

let intersections = fs.readFileSync('15.dat', 'utf-8')
    .split('\n')
    .map(line => line.matchAll(/-?\d+/g))
    .map(matches => [...matches].map(Number))
    .map(intersectLine)
    .filter(([a, b]) => a <= b)
    .flat()

// no need to merge segments since they all overlap
let ans = Math.max(...intersections) - Math.min(...intersections)
console.log(ans);
assert(ans === 5525847)