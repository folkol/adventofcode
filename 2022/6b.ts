import * as fs from "fs";

const N = 14;
let ans = N, bytes = fs.readFileSync('6.dat')
while (new Set(bytes.subarray(ans - N, ans)).size < N)
    ans++
console.log(ans)