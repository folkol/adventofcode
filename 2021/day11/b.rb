files = File.readlines "input.dat", :chomp => true
numbers = files.map { |line| line.scan(/[[:digit:]]/).map(&:to_i) }
$num_flashes = 0

def buff_neighbours(grid, i, j)
  a = [-1, 0, 1]
  a.product(a).each do |di, dj|
    x, y = i + di, j + dj
    grid[x][y] += 1 if x.between?(0, 9) and y.between?(0, 9)
  end
end

def step(grid)
  did_flash = []
  grid.each_with_index do |line, row|
    line.each_with_index do |n, col|
      grid[row][col] = n + 1
    end
  end
  while true
    new_flashes = false
    grid.each_with_index do |line, row|
      line.each_with_index do |n, col|
        current = row * 10 + col
        if n > 9 and not did_flash.include? current
          $num_flashes += 1
          did_flash << current
          buff_neighbours(grid, row, col)
          new_flashes = true
        end
      end
    end
    if !new_flashes
      break
    end
  end

  grid.each_with_index do |line, row|
    line.each_with_index do |n, col|
      current = row * 10 + col
      if did_flash.include? current
        grid[row][col] = 0
      end
    end
  end

  return did_flash.length
end

loop.with_index(1) do |_, i|
  if step(numbers) == 100
    p "All did flash at step #{i}!"
    break
  end
end
