use std::collections::HashSet;
use std::fs;

type Grid = Vec<Vec<char>>;
type Beams = HashSet<(usize, usize)>;

fn main() {
    let data = fs::read_to_string("input.dat").expect("Failed to read input");
    let grid: Vec<Vec<char>> = data.lines().map(|line| line.chars().collect()).collect();
    let s = find_starting_position(&grid);
    let h = grid.len();
    let w = grid[0].len();

    let mut ans = 0;
    let mut beams = HashSet::from([s]);
    while !beams.is_empty() {
        let mut next_beams = HashSet::new();
        for (i_prev, j_prev) in beams {
            let (i, j) = (i_prev + 1, j_prev as i32);
            if i >= h {
                continue;
            }

            match grid[i][j as usize] {
                '.' => {
                    next_beams.insert((i, j as usize));
                }
                '^' => {
                    ans += 1;
                    insert_if_on_grid(h, w, &mut next_beams, i, j - 1);
                    insert_if_on_grid(h, w, &mut next_beams, i, j + 1);
                }
                c => panic!("Unexpected character: '{c}'"),
            };
        }
        beams = next_beams;
    }
    println!("{}", ans);
}

fn insert_if_on_grid(w: usize, h: usize, beams: &mut Beams, i: usize, j: i32) {
    if i < h && j >= 0 && j < w as i32 {
        beams.insert((i, j as usize));
    }
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
