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

let n = 0

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

function traverse(openValves: string[], pos: string, remainingTime: number, flow: number, p: any[]) {
    // console.log(p.join(''))
    // if (p.join('') === 'AADDBBJJHHEECC') {
    //     console.log('wut')
    // }
    if (flow > maxFlow) {  // do not require us to land at 'opened valve' at the very last step
        console.log('New maximum', flow, p)
        maxPath = [...p.slice(), pos]
        maxFlow = flow
    }
    let upperBound = openValves.reduce((acc, x) => {
        let n = graph.find(node => node[0] === x)
        return acc + n[1]
    }, 0);
    if (flow + (remainingTime + 1) * upperBound < maxFlow) {
        // console.log('Wrong path')
        return
    }
    for (let valve of openValves) {
        let distance = bfs(pos, valve);
        if (distance > remainingTime) {
            continue
        }
        // console.log('Distance', pos, valve, distance)
        let n = graph.find(node => node[0] === valve);
        let remainingValves = openValves.filter((name) => name !== valve);
        traverse(remainingValves, valve, remainingTime - distance - 1, flow + (remainingTime - distance - 1) * n[1], [...p, pos]);
    }
}

let openValves = graph.filter(node => node[1] > 0).map(node => node[0]);
traverse(openValves, 'AA', 30, 0, []) // and also 'open set'?
console.log(maxFlow, maxPath)

// assert(maxFlow > 1697)
// assert(maxFlow > 1743)
assert(maxFlow === 1767)
