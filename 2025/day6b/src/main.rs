use std::fs;

fn main() {
    let data = fs::read_to_string("input.dat").expect("Unable to read file");
    let grid: Vec<Vec<char>> = data.lines().map(|x| x.chars().collect()).collect();
    let width = grid[0].len();
    let height = grid.len();

    let mut ans = 0;
    let mut numbers = Vec::new();
    for col in (0..width).rev() {
        let mut n: u64 = 0;
        for row in 0..height {
            let c = grid[row][col];
            if c.is_numeric() {
                let lsd = c.to_digit(10).expect("Invalid digit") as u64;
                n = n * 10 + lsd;
            } else if c == '*' {
                ans += n * numbers.iter().product::<u64>();
                numbers.clear();
            } else if c == '+' {
                ans += n + numbers.iter().sum::<u64>();
                numbers.clear();
            } else if row == height - 1 && n > 0 {
                numbers.push(n);
            }
        }
    }
    println!("{}", ans);
}
