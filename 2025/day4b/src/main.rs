use std::fs;

const FORK_LIFT_CUTOFF: usize = 4;

type Grid = Vec<Vec<char>>;

fn main() {
    let data = fs::read_to_string("input.dat").expect("Unable to read file");
    let mut grid: Grid = data.lines().map(|line| line.chars().collect()).collect();

    let mut ans = 0;

    loop {
        let mut movable: Vec<(usize, usize)> = Vec::new();
        for (i, row) in grid.iter().enumerate().clone() {
            for (j, &cell) in row.iter().enumerate().clone() {
                let can_move = cell == '@' && can_access(&grid, i, j);
                if can_move {
                    movable.push((i, j));
                }
            }
        }
        if movable.is_empty() {
            break;
        }
        for (i, j) in movable.drain(..) {
            ans += 1;
            grid[i][j] = '.';
        }
    }

    println!("{ans}");
}

fn can_access(grid: &Grid, i: usize, j: usize) -> bool {
    let rows = grid.len();
    let cols = grid[0].len();
    let num_rolls = neighbors(i, j, rows, cols)
        .filter(|&(ni, nj)| grid[ni][nj] == '@')
        .count();
    num_rolls < FORK_LIFT_CUTOFF
}

fn neighbors(i: usize, j: usize, rows: usize, cols: usize) -> impl Iterator<Item = (usize, usize)> {
    #[rustfmt::skip]
    const OFFSETS: [(i32, i32); 8] = [
        (-1,-1), (-1,0), (-1,1),
        ( 0,-1),         ( 0,1),
        ( 1,-1), ( 1,0), ( 1,1),
    ];

    OFFSETS.into_iter().filter_map(move |(di, dj)| {
        let ni = i as i32 + di;
        let nj = j as i32 + dj;
        if ni >= 0 && nj >= 0 && ni < rows as i32 && nj < cols as i32 {
            Some((ni as usize, nj as usize))
        } else {
            None
        }
    })
}
