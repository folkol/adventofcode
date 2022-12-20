import * as fs from "fs";
import * as assert from "assert";

function clamp(m: number, k: number) {
    return (m % k + k) % k;
}

function swap(xs: number[][], m: number, index: number) {
    let tmp = xs[clamp(m, xs.length)];
    xs[clamp(m, xs.length)] = xs[clamp(index, xs.length)];
    xs[clamp(index, xs.length)] = tmp;
}

function slide(xs: number[][], index: number, steps: number, direction: number) {
    for (let i = 0; i < steps; i++) {
        swap(xs, index + direction, index);
        index += direction;
    }
}

function mix(numbers: number[]): number[] {
    let numbersWithIndex = numbers.map((e, i) => [e, i])
    for (let id = 0; id < numbersWithIndex.length; id++) {
        let value = numbers[id];
        let index = numbersWithIndex.findIndex(([_, i]) => i === id);
        slide(numbersWithIndex, index, Math.abs(value), Math.sign(value))
    }
    return numbersWithIndex.map(([e, _]) => e);
}

let numbers = fs.readFileSync('20.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(Number);

numbers = mix(numbers)

let offset = numbers.indexOf(0)
let a = numbers[clamp(offset + 1000, numbers.length)];
let b = numbers[clamp(offset + 2000, numbers.length)];
let c = numbers[clamp(offset + 3000, numbers.length)];
let ans = a + b + c;
console.log(ans)
assert(ans === 11616)
