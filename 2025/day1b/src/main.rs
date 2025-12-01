use std::fs::File;
use std::io::{self, BufRead};

const INITIAL_POS: i32 = 50;
const PERIOD: i32 = 100;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let file = File::open("input.dat")?;

    let code: i32 = io::BufReader::new(file)
        .lines()
        .flatten()
        .scan(INITIAL_POS, |dial_position, line| {
            let (tag, n) = line.split_at(1);
            let ticks: i32 = n.parse().ok()?;
            let delta = if tag == "L" { -1 } else { 1 };
            let mut at_zeros = 0;
            for _ in 0..ticks {
                *dial_position = (*dial_position + delta).rem_euclid(PERIOD);
                if *dial_position == 0 {
                    at_zeros += 1;
                }
            }
            Some(at_zeros)
        })
        .sum();

    println!("CODE: {}", code);
    Ok(())
}
