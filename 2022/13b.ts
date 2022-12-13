import * as fs from "fs";
import * as assert from "assert";

type node = number | node[]

function parseNumber(line: string, pos: number): [node, number] {
    let s = line.slice(pos);
    let m = s.match(/\d+/)[0];
    return [Number(m), pos + m.length]
}

function parseList(line: string, pos: number): [node, number] {
    let elements = []
    while (line[pos] !== ']') {
        let [child, nextPos] = parse(line, pos);
        elements.push(child)
        if (line[nextPos] === ',') {
            nextPos++
        }
        pos = nextPos;
    }
    return [elements, pos + 1]
}

function parse(line: string, pos: number): [node, number] {
    if (line[pos] === '[') {
        return parseList(line, pos + 1);
    } else {
        return parseNumber(line, pos);
    }
}

function ordered(left: number | node[], right: number | node[]) {
    if (typeof left === 'number' && typeof right === 'number') {
        if (left < right) {
            return -1
        } else if (left > right) {
            return 1
        } else {
            return 0
        }
    } else if (typeof left === 'object' && typeof right === 'object') {
        for (let i = 0; i < left.length && i < right.length; i++) {
            let x = ordered(left[i], right[i]);
            if (x)
                return x
        }
        if (left.length < right.length) {
            return -1
        }
        if (left.length > right.length) {
            return 1
        }
        return 0;
    } else if (typeof left === 'object' && typeof right === 'number') {
        return ordered(left, [right])
    } else if (typeof left === 'number' && typeof right === 'object') {
        return ordered([left], right)
    }
}

let ast = fs.readFileSync('13.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .filter(line => line)
    .map(line => parse(line, 0)[0])
ast.push([[2]])
ast.push([[6]])

ast.sort((a, b) => ordered(a, b))

let dp1 = 1 + ast.findIndex(s => JSON.stringify(s) === '[[2]]');
let dp2 = 1 + ast.findIndex(s => JSON.stringify(s) === '[[6]]');
let ans = dp1 * dp2;
console.log(ans)
assert(ans === 22134)