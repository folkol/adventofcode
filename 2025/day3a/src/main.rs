use std::fs;

fn max_joltage(line: &str) -> u32 {
    let digits: Vec<_> = line.chars().filter_map(|c| c.to_digit(10)).collect();
    let l = digits.len();
    let mut a = digits[l - 2];
    let mut b = digits[l - 1];

    for &d in digits[..l - 2].iter().rev() {
        if d >= a {
            b = a;
            a = d;
        } else if d > b {
            b = d;
        }
    }

    a * 10 + b
}

fn main() {
    let n: u32 = fs::read_to_string("input.dat")
        .expect("Could not read input.dat")
        .lines()
        .map(max_joltage)
        .sum();
    println!("{:?}", n);
}
