use std::fs;

fn recover(line: &str) -> u32 {
    let first = line.chars().find(char::is_ascii_digit).unwrap();
    let last = line.chars().rfind(char::is_ascii_digit).unwrap();
    format!("{}{}", first, last).parse().unwrap()
}

fn main() {
    let answer: u32 = fs::read_to_string("input.dat").unwrap()
        .lines()
        .map(recover)
        .sum();
    println!("{}", answer);
}
