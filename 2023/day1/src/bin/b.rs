use std::fs;
use std::iter::Iterator;

const WORDS: &[&str] = &[
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn match_digit(slice: &str) -> Option<usize> {
    WORDS.iter().enumerate().find_map(|(x, &word)| {
        let value = x + 1;
        if slice.starts_with(word) || slice.starts_with(&value.to_string()) {
            return Some(value);
        };
        None
    })
}

fn first_digit(line: &str) -> usize {
    for n in 0..line.len() {
        if let Some(digit) = match_digit(&line[n..]) {
            return digit;
        }
    }
    panic!("Unexpected input, there should be at least one digit");
}

fn last_digit(line: &str) -> usize {
    for n in (0..line.len()).rev() {
        if let Some(digit) = match_digit(&line[n..]) {
            return digit;
        }
    }
    panic!("Unexpected input, there should be at least one digit");
}

fn recover(line: &str) -> usize {
    first_digit(line) * 10 + last_digit(line)
}

fn main() {
    let answer: usize = fs::read_to_string("input.dat")
        .unwrap()
        .lines()
        .map(recover)
        .sum();
    println!("{}", answer); // 54770
}
