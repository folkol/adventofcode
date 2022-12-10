import * as fs from "fs";
import {strict as assert} from "assert";

let prog = fs.readFileSync('10.dat', 'utf-8')
    .split('\n')
    .map(line => line.split(' '))
    .flatMap(([op, arg]) => op === 'addx' ? [[op, Number(arg)], ['noop']] : [[op]]);

let ans = 0;
for (let cycle = 1, register = 1; cycle < prog.length; cycle++) {
    if ((cycle + 20) % 40 === 0) {
        ans += register * cycle;
    }
    let [op, arg] = prog[cycle - 2] || ['noop'];
    if (op === 'addx') {
        register += arg as number
    }
}
console.log(ans)
assert(ans === 13720)