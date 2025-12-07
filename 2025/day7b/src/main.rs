use std::collections::HashMap;
use std::fs;

type Grid = Vec<Vec<char>>;
type Memo = HashMap<(usize, i32), usize>;

fn main() {
    let grid: Vec<Vec<char>> = fs::read_to_string("input.dat")
        .expect("Failed to read input")
        .lines()
        .map(|line| line.chars().collect())
        .collect();
    let (i, j) = find_starting_position(&grid);

    let timelines = 1 + count_timelines(i, j as i32, &grid, &mut HashMap::new());
    println!("{timelines}");
}

fn count_timelines(i: usize, j: i32, grid: &Grid, memo: &mut Memo) -> usize {
    if let Some(&count) = memo.get(&(i, j)) {
        return count;
    }

    if j < 0 {
        return 0;
    }

    let Some(row) = grid.get(i) else {
        return 0;
    };

    let Some(&cell) = row.get(j as usize) else {
        return 0;
    };

    let count = match cell {
        '.' | 'S' => count_timelines(i + 1, j, grid, memo),
        '^' => 1 + count_timelines(i, j - 1, grid, memo) + count_timelines(i, j + 1, grid, memo),
        c => panic!("invalid character: {c}"),
    };

    memo.insert((i, j), count);
    count
}

fn find_starting_position(grid: &Grid) -> (usize, usize) {
    for (i, row) in grid.iter().enumerate() {
        for (j, c) in row.iter().enumerate() {
            if *c == 'S' {
                return (i, j);
            }
        }
    }
    panic!("No starting position found");
}
