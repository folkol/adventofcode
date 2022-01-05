import Foundation

func convolve(algorithm: [Int], lines: [[Int]]) -> [[Int]] {
    func outputFor(i: Int, j: Int) -> Int {
        var nums: [Int] = []
        for di in -1..<2 {
            for dj in -1..<2 {
                if 0...(lines.count - 1) ~= (i + di) && 0...(lines[0].count - 1) ~= (j + dj) {
                    nums.append(lines[i + di][j + dj])
                } else {
                    nums.append(lines[0][0])
                }
            }
        }
        let s = nums.map(String.init).joined(separator: "")
        let integer = Int(s, radix: 2)!
        return algorithm[integer]
    }

    return lines.enumerated().map({ (i, s) in
        s.enumerated().map { (j, character) in
            outputFor(i: i, j: j)
        }
    })
}

private func parse(input: String, paddingAmount: Int = 10) -> ([Int], [[Int]]) {
    let data = input.split(separator: "\n")
    let algorithm = data[0].map {
        $0 == "#" ? 1 : 0
    }
    let lines = data[1...]

    let blank = Array(repeating: 0, count: lines.first!.count + 2 * paddingAmount)
    let padding = Array(repeating: 0, count: paddingAmount)
    var image: [[Int]] = []
    for _ in 0..<paddingAmount {
        image.append(blank)
    }
    for line in lines {
        let numbers = line.map {
            $0 == "#" ? 1 : 0
        }
        image.append(padding + numbers + padding)
    }
    for _ in 0..<paddingAmount {
        image.append(blank)
    }

    return (algorithm, image)
}

let input = try! String(contentsOfFile: "input.dat")
var (algorithm, image) = parse(input: input, paddingAmount: 50)
for _ in 0..<50 {
    image = convolve(algorithm: algorithm, lines: image)
}
//image = convolve(algorithm: algorithm, lines: image)
let ans = image.flatMap({ $0 }).reduce(0) {
    $0 + $1
}
print(ans)
