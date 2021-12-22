package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
)

type Edge struct {
	vertex, weight int
}

type Graph map[int][]Edge
type NodeSet map[int]bool

func readLines() []string {
	scanner := bufio.NewScanner(os.Stdin)
	var lines []string
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		log.Println(err)
	}
	return lines
}

func coordToNode(size int, i int, j int) int {
	return i*size + j
}

func readGraph() Graph {
	lines := readLines()
	size := len(lines)

	var seedWeights [][]int
	for _, row := range lines {
		var temp []int
		for _, weight := range row {
			temp = append(temp, int(weight-'0'))
		}
		seedWeights = append(seedWeights, temp)
	}

	var weights [][]int
	for i := 0; i < 5; i++ {
		for k := 0; k < size; k++ {
			var temp []int
			for j := 0; j < 5; j++ {
				for l := 0; l < size; l++ {
					var weight = seedWeights[k][l] + i + j
					for weight > 9 {
						weight -= 9
					}
					temp = append(temp, weight)
				}
			}
			weights = append(weights, temp)
		}
	}

	graph := make(Graph)
	for i, row := range weights {
		for j, weight := range row {
			n := coordToNode(size*5, i, j)
			for _, m := range neighbours(i, j, size*5) {
				graph[m] = append(graph[m], Edge{n, weight})
			}
		}
	}
	return graph
}

func neighbours(i int, j int, size int) []int {
	var ret []int
	if i > 0 {
		ret = append(ret, coordToNode(size, i-1, j))
	}
	if i < size-1 {
		ret = append(ret, coordToNode(size, i+1, j))
	}
	if j > 0 {
		ret = append(ret, coordToNode(size, i, j-1))
	}
	if j < size-1 {
		ret = append(ret, coordToNode(size, i, j+1))
	}

	return ret
}

func popMin(queue map[int]bool, distance map[int]int) int {
	var cur = -1
	for n := range queue {
		if cur == -1 || distance[n] < distance[cur] {
			cur = n
		}
	}
	delete(queue, cur)
	return cur
}

func main() {
	graph := readGraph()

	distance := make(map[int]int)
	for i := range graph {
		distance[i] = math.MaxInt32
	}
	distance[0] = 0

	visited := make(NodeSet)
	queue := make(NodeSet)
	queue[0] = true
	for len(queue) > 0 {
		cur := popMin(queue, distance)
		for _, edge := range graph[cur] {
			if _, exists := visited[edge.vertex]; !exists {
				queue[edge.vertex] = true
				candidateWeight := distance[cur] + edge.weight
				if candidateWeight < distance[edge.vertex] {
					distance[edge.vertex] = candidateWeight
				}
			}
		}
		visited[cur] = true
	}

	fmt.Println(distance[len(graph)-1])
}
