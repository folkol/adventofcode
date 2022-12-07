import * as fs from "fs";
import {strict as assert} from "assert";

let parent: Record<string, string> = {}
let cwd: string[] = []
let du: Record<string, number> = {};
fs.readFileSync('7.dat', 'utf-8').trimEnd().split('\n').forEach(line => {
    let [a, b, c] = line.split(' ')
    if (a === '$') {
        if (b === 'cd' && c === '/') {
            cwd = []
        } else if (b === 'cd' && c === '..') {
            cwd.pop();
        } else if (b === 'cd') {
            let dirname = cwd.join('/')
            cwd.push(c)
            parent[cwd.join('/')] = dirname
        }
    } else if (a.match(/\d+/)) {
        let path = cwd.join('/')
        while (path !== undefined) {
            du[path] = Number(a) + (du[path] || 0)
            path = parent[path];
        }
    }
})
let missingSpace = 30000000 - (70000000 - du['']);
let victim = Object.values(du).sort((a, b) => a - b).find((size) => size >= missingSpace) || 0
console.log(victim)
assert(victim === 6296435)