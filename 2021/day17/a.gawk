match($0, "target area: x=-?[0-9]+[.]{2}-?[0-9]+, y=(-?[0-9]+)[.].*+", groups) {
    bottom_line=groups[1]
    ans=(bottom_line^2 + bottom_line) / 2  # Courtesy of Gauss
    print(ans)
}
