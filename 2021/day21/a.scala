object a {
  var numRolls = 0

  private def roll() = {
    numRolls = numRolls + 1
    (numRolls - 1) % 100 + 1
  }

  def play(p1: Int, p2: Int, s1: Int, s2: Int): Int = {
    if (s2 >= 1000) {
      return s1 * numRolls
    }

    val pos = (p1 + roll() + roll() + roll() - 1) % 10 + 1
    play(p2, pos, s2, s1 + pos)
  }

  def main(positions: Array[String]): Unit = {
    if (positions.length != 2) {
      println("Expected 2 arguments, pos 1 and pos 2")
      sys.exit(1)
    }
    println(play(positions(0).toInt, positions(1).toInt, 0, 0))
  }
}
