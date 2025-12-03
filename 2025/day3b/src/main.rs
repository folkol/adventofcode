use std::fs;

const K: usize = 12;

fn max_joltage(line: &str) -> u64 {
    let digits: Vec<u32> = line.chars().filter_map(|b| b.to_digit(10)).collect();

    let mut wiggle_room = digits.len() - K;
    let mut candidate: Vec<u32> = Vec::with_capacity(digits.len());

    for d in digits {
        while wiggle_room > 0 && candidate.last().is_some_and(|&x| x < d) {
            candidate.pop();
            wiggle_room -= 1;
        }
        candidate.push(d);
    }

    candidate.truncate(K);
    candidate
        .into_iter()
        .fold(0u64, |acc, d| acc * 10 + d as u64)
}

fn main() {
    let n: u64 = fs::read_to_string("input.dat")
        .expect("Could not read input.dat")
        .lines()
        .map(max_joltage)
        .sum();
    println!("{:?}", n); // 173065202451341
}
