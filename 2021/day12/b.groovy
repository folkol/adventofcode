class Graph {
    private Map<String, List<String>> map = [:]

    void addEdge(String key, String value) {
        List list = map.get(key, [])
        list.add(value)
        map[key] = list
    }

    def paths(start, end) {
        pathsInternal([start], end, [])
    }

    private static def duplicate(List<String> seen) {
        seen.countBy { it }.any { node, count -> count > 1 && !largeCave(node) }
    }

    private static boolean largeCave(String neighbour) {
        Character.isUpperCase(neighbour.charAt(0))
    }

    private def pathsInternal(List<String> seen, destination, List<List<String>> acc) {
        for (neighbour in map[seen.last()]) {
            if (largeCave(neighbour)) {
                pathsInternal(seen + [neighbour], destination, acc)
                continue
            }

            if (neighbour == 'start') {
                continue
            }

            def seenCount = seen.count(neighbour)
            if (neighbour == 'end') {
                acc.add(seen + [neighbour])
            } else if (seenCount == 0) {
                pathsInternal(seen + [neighbour], destination, acc)
            } else if (seenCount == 1 && !duplicate(seen)) {
                pathsInternal(seen + [neighbour], destination, acc)
            }
        }

        acc
    }
}

Graph g = new Graph();
System.in.eachLine {
    def (String a, String b) = it.tokenize('-')
    g.addEdge(a, b)
    g.addEdge(b, a)
}

print(g.paths('start', 'end').size())
