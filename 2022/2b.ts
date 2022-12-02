import * as fs from 'node:fs';
import {strict as assert} from 'node:assert';

let shapeValues: { [key: string]: number } = {
    'A': 0,
    'X': 0,
    'B': 1,
    'Y': 1,
    'C': 2,
    'Z': 2,
}

function roundScore(ours: number, theirs: number): number {
    let shapeDiff = (ours - theirs + 3) % 3;
    if (shapeDiff === 0) {
        return 3;
    } else if (shapeDiff === 1) {
        return 6;
    } else {
        return 0;
    }
}

function shapeForOutcome(outcome: number, theirs: number) {
    if (outcome === 1) {
        return theirs;
    } else if (outcome === 2) {
        return (theirs + 1 + 3) % 3;
    } else {
        return (theirs - 1 + 3) % 3;
    }
}

let data = fs.readFileSync('2.dat', 'utf-8');
let roundScores = data.split('\n').map((line: string): number => {
    let [theirs, outcome] = line.split(' ').map((shape) => shapeValues[shape]);
    let ours = shapeForOutcome(outcome, theirs);
    return roundScore(ours, theirs) + ours + 1
});
let totalScore = roundScores.reduce((acc: number, x: number) => acc + x);
console.log(totalScore);
assert(totalScore === 14060);
