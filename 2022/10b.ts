import * as fs from "fs";

let prog = fs.readFileSync('10.dat', 'utf-8')
    .split('\n')
    .map(line => line.split(' '))
    .flatMap(([op, arg]) => op === 'addx' ? [[op, Number(arg)], ['noop']] : [[op]]);

for (let cycle = 0, x = 1; cycle < prog.length; cycle++) {
    let beam = cycle % 40;
    let spriteHit = beam === x - 1 || beam === x || beam === x + 1;
    process.stdout.write(spriteHit ? '⬛' : '🟩')
    if (beam === 39) {
        console.log()
    }
    let [op, arg] = prog[cycle - 1] || ['noop'];
    if (op === 'addx') {
        x += arg as number
    }
}
// FBURHZCH