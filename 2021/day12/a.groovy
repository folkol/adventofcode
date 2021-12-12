class Graph {
    private Map<String, List<String>> map = [:]

    void addEdge(String key, String value) {
        List list = map.get(key, [])
        list.add(value)
        map[key] = list
    }

    def paths(start, end) {
        return pathsInternal([], start, end, [])
    }

    private def pathsInternal(List<String> seen, node, destination, List<List<String>> acc) {
        if (node == destination) {
            acc.add(seen + [node])
            return
        }
        for (neighbour in map[node]) {
            if (Character.isUpperCase(neighbour.charAt(0)) || !seen.contains(neighbour)) {
                pathsInternal(seen + [node], neighbour, destination, acc)
            }
        }
        return acc
    }
}

Graph g = new Graph();
new File('input.dat').each { line ->
    def (String a, String b) = line.split('-')
    g.addEdge(a, b)
    g.addEdge(b, a)
}

print(g.paths('start', 'end').size())
