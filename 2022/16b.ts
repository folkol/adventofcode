import * as fs from "fs";
import * as assert from "assert";

type Node = [string, number, string[]]

// TODO: Construct DAG with node x day and traverse that?

function parseNode(line: string): Node {
    let [node, flow, ...neighbours] = [...line.matchAll(/[A-Z]{2}|\d+/g)].map(line => line[0]);
    return [node, Number(flow), neighbours];
}

let graph: Node[] = fs.readFileSync('16.dat', 'utf-8')
    .trimEnd()
    .split('\n')
    .map(parseNode);

let maxFlow = 0;
let maxPath = []

let capacity = graph.reduce((acc, x) => acc + x[1], 0)

let numCalls = 0

function bfs(pos: string, valve: string) {
    let seen = new Set<string>();
    let queue = [[pos, 0]]
    while (queue.length > 0) {
        let [nodeName, cost]: [string, number] = queue.shift() as [string, number];
        if (nodeName === valve) {
            return cost
        }
        seen.add(nodeName)
        let node = graph.find(node => node[0] === nodeName);
        for (let neighbor of node[2]) {
            // console.log('Considering', neighbor, cost + 1)
            if (!seen.has(neighbor)) {
                queue.push([neighbor, cost + 1])
            }
        }
    }
}

let dag = [
    ['0', 0, []]
];
for (let i = 30; i > 0; i--) {
    for (let node of graph.filter(node => node[1] > 0)) {
        let [name, flow, neighbors] = node;
        let dailyNode = [`${name}-${i}`, flow * (i - 1) || 0, ['0', ...(neighbors.map(neighbor => `${neighbor}-${i - 1}`))]]
        dag.push(dailyNode)
    }
}
console.log(dag)

function traverse(openValves: string[], pos: string[], remainingTime: number[], flow: number[], upperBound: number) {
    if (flow[0] < 0 || flow[1] < 0) {
        console.log('wut')
    }
    if (remainingTime[0] < 0 || remainingTime[1] < 0) {
        console.log('wat')
    }
    if (numCalls++ % 10000000 === 0) {
        console.log(numCalls, openValves, pos, remainingTime, flow, upperBound);
    }
    // console.log(p.join(''))
    // if (p.join('') === 'AADDBBJJHHEECC') {
    //     console.log('wut')
    // }
    if (flow[0] + flow[1] > maxFlow) {  // do not require us to land at 'opened valve' at the very last step
        console.log('New maximum', flow, upperBound, openValves);
        maxFlow = flow[0] + flow[1];
    }
    // let upperBound = openValves.reduce((acc, x) => {
    //     let n = graph.find(node => node[0] === x)
    //     return acc + n[1]
    // }, 0);
    if (flow[0] + flow[1] + Math.max(remainingTime[0], remainingTime[1]) * upperBound < maxFlow ) {
        // console.log('Wrong path')
        return
    }

    if (openValves.length === 1) {
        let valve = openValves[0]
        // let distanceA = bfs(pos[0], valve);
        let distanceA = distances.get(pos[0]).get(valve)
        // let distanceB = bfs(pos[1], valve);
        let distanceB = distances.get(pos[1]).get(valve)
        let nA = graph.find(node => node[0] === valve);
        if (!nA) {
            console.log('wut')
            process.exit(1)
        }
        if (distanceA <= remainingTime[0]) {
            traverse(
                [],
                [valve, pos[1]],
                [remainingTime[0] - distanceA - 1, remainingTime[1]],
                [flow[0] + (remainingTime[0] - distanceA - 1) * nA[1], flow[1]],
                upperBound - nA[1]
            );
        }
        if (distanceB <= remainingTime[0]) {
            traverse(
                [],
                [pos[1], valve],
                [remainingTime[0], remainingTime[1] - distanceA - 1],
                [flow[0], flow[1] + (remainingTime[1] - distanceA - 1) * nA[1]],
                upperBound - nA[1]
            );
        }
    } else {
        for (let valveA of openValves) {
            for (let valveB of openValves) {
                if (valveA === valveB) {
                    continue
                }

                let nextPos = pos.slice();
                let nextRemainingTime = remainingTime.slice();
                let nextFlow = flow.slice()
                let nextOpenValves = openValves.slice();

                // let distanceA = bfs(pos[0], valveA);
                let foo = 0
                let distanceA = distances.get(pos[0]).get(valveA)
                if (distanceA < remainingTime[0]) {
                    let n = graph.find(node => node[0] === valveA);
                    nextPos[0] = valveA;
                    nextRemainingTime[0] = remainingTime[0] - distanceA - 1
                    nextFlow[0] = flow[0] + (remainingTime[0] - distanceA - 1) * n[1]
                    foo += n[1]
                    nextOpenValves = nextOpenValves.filter((name) => name !== valveA);
                }
                // let distanceB = bfs(pos[1], valveB);
                let distanceB = distances.get(pos[1]).get(valveB)
                if (distanceB < remainingTime[1]) {
                    let n = graph.find(node => node[0] === valveB);
                    nextPos[1] = valveB;
                    nextRemainingTime[1] = remainingTime[1] - distanceB - 1
                    nextFlow[1] = flow[1] + (remainingTime[1] - distanceB - 1) * n[1]
                    foo += n[1]
                    nextOpenValves = nextOpenValves.filter((name) => name !== valveB);
                }

                if (openValves.length !== nextOpenValves.length) {
                    traverse(nextOpenValves, nextPos, nextRemainingTime, nextFlow, upperBound - foo);
                }
            }
        }
    }
}

let distances = new Map<string, Map<string, number>>();
for (let from of graph) {
    for (let to of graph) {
        let x = distances.get(from[0]) || new Map<string, number>();
        let distance = bfs(from[0], to[0]);
        x.set(to[0], distance);
        distances.set(from[0], x)
    }
}

let sort = graph.filter(node => node[1] > 0).sort((a, b) => b[1] - a[1]);
let openValves = sort.map(node => node[0]);
let upperBound = openValves.reduce((acc, x) => {
    let n = graph.find(node => node[0] === x)
    return acc + n[1]
}, 0);
traverse(openValves, ['AA', 'AA'], [26, 26], [0, 0], upperBound) // and also 'open set'?
console.log(maxFlow, maxPath)

// assert(maxFlow > 1697)
// assert(maxFlow > 1743)
assert(maxFlow < 2497)
