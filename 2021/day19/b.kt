import java.io.File
import kotlin.math.absoluteValue
import kotlin.math.max

typealias Vector = Triple<Int, Int, Int>
typealias Matrix = Triple<Vector, Vector, Vector>

private operator fun Matrix.times(vector: Vector): Vector {
    val (a, b, c) = this.first
    val (d, e, f) = this.second
    val (g, h, i) = this.third
    val (x, y, z) = vector
    return Vector(
        a * x + b * y + c * z,
        d * x + e * y + f * z,
        g * x + h * y + i * z
    )
}

private operator fun Vector.plus(other: Vector): Vector {
    return Vector(this.first + other.first, this.second + other.second, this.third + other.third)
}

private operator fun Vector.minus(other: Vector): Vector {
    return Vector(this.first - other.first, this.second - other.second, this.third - other.third)
}

fun readScanners(): MutableMap<Int, MutableList<Vector>> {
    val scanners: MutableMap<Int, MutableList<Vector>> = HashMap()
    var scanner: MutableList<Vector> = ArrayList()
    var n = 0
    File("day19/input.dat").forEachLine {
        if (it.startsWith("---")) {
            scanner = ArrayList()
        } else if (it.isBlank()) {
            scanners[n] = scanner
            n++
        } else {
            val (x, y, z) = it.split(",")
            scanner.add(Vector(x.toInt(), y.toInt(), z.toInt()))
        }
    }
    scanners[n] = scanner
    return scanners
}

fun bases(): List<Matrix> {
    // generated by taking unique results from rotating I around all axis
    return listOf(
        Matrix(Vector(-1, 0, 0), Vector(0, -1, 0), Vector(0, 0, 1)),
        Matrix(Vector(-1, 0, 0), Vector(0, 0, -1), Vector(0, -1, 0)),
        Matrix(Vector(-1, 0, 0), Vector(0, 0, 1), Vector(0, 1, 0)),
        Matrix(Vector(-1, 0, 0), Vector(0, 1, 0), Vector(0, 0, -1)),
        Matrix(Vector(0, -1, 0), Vector(-1, 0, 0), Vector(0, 0, -1)),
        Matrix(Vector(0, -1, 0), Vector(0, 0, -1), Vector(1, 0, 0)),
        Matrix(Vector(0, -1, 0), Vector(0, 0, 1), Vector(-1, 0, 0)),
        Matrix(Vector(0, -1, 0), Vector(1, 0, 0), Vector(0, 0, 1)),
        Matrix(Vector(0, 0, -1), Vector(-1, 0, 0), Vector(0, 1, 0)),
        Matrix(Vector(0, 0, -1), Vector(0, -1, 0), Vector(-1, 0, 0)),
        Matrix(Vector(0, 0, -1), Vector(0, 1, 0), Vector(1, 0, 0)),
        Matrix(Vector(0, 0, -1), Vector(1, 0, 0), Vector(0, -1, 0)),
        Matrix(Vector(0, 0, 1), Vector(-1, 0, 0), Vector(0, -1, 0)),
        Matrix(Vector(0, 0, 1), Vector(0, -1, 0), Vector(1, 0, 0)),
        Matrix(Vector(0, 0, 1), Vector(0, 1, 0), Vector(-1, 0, 0)),
        Matrix(Vector(0, 0, 1), Vector(1, 0, 0), Vector(0, 1, 0)),
        Matrix(Vector(0, 1, 0), Vector(-1, 0, 0), Vector(0, 0, 1)),
        Matrix(Vector(0, 1, 0), Vector(0, 0, -1), Vector(-1, 0, 0)),
        Matrix(Vector(0, 1, 0), Vector(0, 0, 1), Vector(1, 0, 0)),
        Matrix(Vector(0, 1, 0), Vector(1, 0, 0), Vector(0, 0, -1)),
        Matrix(Vector(1, 0, 0), Vector(0, -1, 0), Vector(0, 0, -1)),
        Matrix(Vector(1, 0, 0), Vector(0, 0, -1), Vector(0, 1, 0)),
        Matrix(Vector(1, 0, 0), Vector(0, 0, 1), Vector(0, -1, 0)),
        Matrix(Vector(1, 0, 0), Vector(0, 1, 0), Vector(0, 0, 1))
    )
}

fun numOverlaps(
    fst: Set<Vector>,
    scanner: List<Vector>,
    basis: Matrix,
    translation: Vector
): Int {
    return scanner.count {
        val foo = basis * it
        val bar = foo + translation
        fst.contains(bar)
    }
}

fun findOverlapping(
    fst: Set<Vector>,
    scanners: Map<Int, List<Vector>>
): Triple<Map.Entry<Int, List<Vector>>, Matrix, Vector> {
    bases().forEach { basis ->
        fst.forEach { u ->
            scanners.forEach { scanner ->
                scanner.value.forEach { v ->
                    val translation = u - basis * v
                    if (numOverlaps(fst, scanner.value, basis, translation) >= 12) {
                        return Triple(scanner, basis, translation)
                    }
                }
            }
        }
    }
    throw Exception("Found no overlaps")
}

fun main() {
    val scanners: MutableMap<Int, MutableList<Vector>> = readScanners()
    val fst: MutableSet<Vector> = scanners.remove(0)?.toMutableSet()!!
    val scannerPositions: MutableList<Vector> = ArrayList()
    while (scanners.isNotEmpty()) {
        println("#scanners: ${scanners.size} #fst: ${fst.size}")
        val findOverlapping = findOverlapping(fst, scanners)
        val (scanner, basis, translation) = findOverlapping
        scannerPositions.add(translation)

        fst.addAll(scanner.value.map { basis * it + translation })
        scanners.remove(scanner.key)
    }
    var maxDistance = 0
    scannerPositions.forEach { a ->
        scannerPositions.forEach { b ->
            maxDistance = max(maxDistance, manhattan(a, b))
        }
    }
    println(maxDistance)
}

fun manhattan(a: Vector, b: Vector): Int {
    return (b.first - a.first).absoluteValue + (b.second - a.second).absoluteValue + (b.third - a.third).absoluteValue
}
