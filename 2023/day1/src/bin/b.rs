use std::{fs, io};

const WORDS: &[&str] = &[
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn match_digit(slice: &str) -> Option<usize> {
    WORDS.iter().enumerate().find_map(|(index, &word)| {
        let value = index + 1;
        if slice.starts_with(word) || slice.starts_with(&value.to_string()) {
            Some(value)
        } else {
            None
        }
    })
}

fn recover(line: &str) -> usize {
    let mut digits = Vec::new();
    for n in 0..line.len() {
        if let Some(digit) = match_digit(&line[n..]) {
            digits.push(digit);
        }
    }
    digits[0] * 10 + digits[digits.len() - 1]
}

fn main() -> Result<(), io::Error> {
    let answer: usize = fs::read_to_string("input.dat")?.lines().map(recover).sum();
    Ok(println!("{}", answer))
}
