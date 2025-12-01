use std::fs::File;
use std::io::{self, BufRead};

const INITIAL_POS: i32 = 50;
const PERIOD: i32 = 100;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input.dat")?;
    let code = io::BufReader::new(file)
        .lines()
        .flatten()
        .scan(INITIAL_POS, |dir, line| {
            let (tag, n) = line.split_at(1);
            let ticks: i32 = n.parse().ok()?;
            *dir += if tag == "L" { -ticks } else { ticks };
            Some(dir.rem_euclid(PERIOD) == 0)
        })
        .filter(|&at_zero| at_zero)
        .count();

    println!("CODE: {}", code);
    Ok(())
}
