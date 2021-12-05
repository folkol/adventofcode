let transpose = m => m[0].map((x, i) => m.map(x => x[i]));
let sum = arr => arr.reduce((acc, n) => acc + n);

let lines = require('fs').readFileSync('input.dat', 'utf-8').split(/\r?\n/);
let numbers = lines.shift().split(',').map(n => parseInt(n));
lines.shift();  // blank line

let boards = [];
let nextBoard = {rows: []};
for (let line of lines) {
    if (line === '') {
        boards.push(nextBoard);
        nextBoard = {rows: []};
    } else {
        let items = line.trim().split(/ +/).map(n => parseInt(n));
        nextBoard.rows.push(items);
    }
}

let marked = [];
for (let draw of numbers) {
    marked.push(draw);
    boards.forEach(board => {
        for (let line of [...board.rows, ...transpose(board.rows)]) {
            if (line.every(n => marked.indexOf(n) !== -1)) {
                let unmarked = board.rows.flatMap(row => row).filter(n => marked.indexOf(n) === -1);
                let score = draw * sum(unmarked);
                console.log(score);
                process.exit(0);
            }
        }
    });
}
