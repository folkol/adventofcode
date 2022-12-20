import * as assert from "assert";
import * as fs from "fs";

function clamp(m: number, k: number) {
    return (m % k + k) % k;
}

function swap(xs: number[][], m: number, index: number) {
    let tmp = xs[clamp(m, xs.length)];
    xs[clamp(m, xs.length)] = xs[clamp(index, xs.length)];
    xs[clamp(index, xs.length)] = tmp;
}

function slide(numbersWithId: number[][], index: number, steps: number, direction: number) {
    let stepsModLength = Math.abs(steps % (numbersWithId.length - 1));
    for (let i = 0; i < stepsModLength; i++) {
        swap(numbersWithId, index + direction, index);
        index += direction;
    }
}

function mix(numbersWithId: [number, number][]) {
    for (let id = 0; id < numbersWithId.length; id++) {
        let value = numbers[id];
        let index = numbersWithId.findIndex(([_, i]) => i === id);
        slide(numbersWithId, index, Math.abs(value), Math.sign(value));
    }
}

let key = 811589153;
let numbers = fs.readFileSync('20.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(Number)
    .map(n => n * key);

let numbersWithIndex: [number, number][] = numbers.map((e, i) => [e, i])
for (let i = 0; i < 10; i++) {
    mix(numbersWithIndex)
}
numbers = numbersWithIndex.map(([e, i]) => e)

let offset = numbers.indexOf(0)
let a = numbers[clamp(offset + 1000, numbers.length)];
let b = numbers[clamp(offset + 2000, numbers.length)];
let c = numbers[clamp(offset + 3000, numbers.length)];
let ans = a + b + c;
console.log(ans)
assert(ans === 9937909178485, ans.toString())
