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
        while (path) {
            du[path] = Number(a) + (du[path] || 0)
            path = parent[path];
        }
    }
})
let ans = Object.values(du).filter(size => size <= 100000).reduce((acc, s) => acc + s);
console.log(ans);
assert(ans === 1350966)
