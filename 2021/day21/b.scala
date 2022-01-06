import scala.collection.mutable

object b {
  val memo = new mutable.HashMap[(Long, Long, Long, Long), (Long, Long)]()

  def countWins(p1: Long, p2: Long, s1: Long, s2: Long): (Long, Long) = {
    val cached = memo.get((p1, p2, s1, s2))
    if (cached.nonEmpty) {
      return cached.get
    }

    if (s2 >= 21) {
      return (1, 0)
    }
    if (s1 >= 21) {
      return (0, 1)
    }

    var w1, w2: Long = 0
    for (d1 <- 1 to 3) {
      for (d2 <- 1 to 3) {
        for (d3 <- 1 to 3) {
          val pos: Long = (p1 + d1 + d2 + d3 - 1) % 10 + 1
          val score: Long = s1 + pos
          val (dw2, dw1) = countWins(p2, pos, s2, score)
          w1 += dw1
          w2 += dw2
        }
      }
    }
    val ans: (Long, Long) = (w1, w2)
    memo.put((p1, p2, s1, s2), ans)
    ans
  }

  def main(positions: Array[String]): Unit = {
    if (positions.length != 2) {
      println("Expected 2 arguments, pos 1 and pos 2")
      sys.exit(1)
    }

    val (w1, w2) = countWins(positions(0).toLong, positions(1).toLong, 0, 0)
    println(w1.max(w2))
  }
}
