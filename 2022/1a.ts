import * as fs from "fs";

let inventory = fs.readFileSync('1.dat', 'utf-8');
let elves: number[] = [];
let current = 0;
inventory.split("\n").forEach(item => {
    if (!item) {
        elves.push(current);
        current = 0;
    } else {
        current += parseInt(item)
    }
});
const maxCalories = Math.max.apply(null, elves);
console.log(maxCalories);
