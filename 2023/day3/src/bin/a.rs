use std::error::Error;
use std::fs;

use regex;
use regex::Regex;

struct Number {
    value: u32,
    lineno: usize,
    begin: usize,
    end: usize,
}

impl Number {
    pub(crate) fn neighborhood(&self, width: usize, height: usize) -> Vec<(u32, u32)> {
        let mut neighbours = Vec::new();
        let top = self.lineno as i32 - 1;
        let bottom = self.lineno as i32 + 1;
        let left = self.begin as i32 - 1;
        let right = self.end as i32 + 1;
        let in_bounds = |i, j| i >= 0 && i < height as i32 && j >= 0 && j < width as i32;
        for row in top..=bottom {
            for col in left..=right {
                if in_bounds(row, col) {
                    neighbours.push((row as u32, col as u32));
                }
            }
        }
        neighbours
    }
}

struct Schematic {
    numbers: Vec<Number>,
    width: usize,
    height: usize,
    data: String,
}

impl Schematic {
    pub(crate) fn get(&self, x: u32, y: u32) -> char {
        let line = self.data.lines().nth(y as usize).unwrap();
        line.chars().nth(x as usize).unwrap()
    }
}

impl From<String> for Schematic {
    fn from(data: String) -> Self {
        let height = data.lines().count();
        let width = data.lines().map(str::len).max().unwrap();
        let numbers = Self::find_numbers(&data);
        Schematic {
            numbers,
            height,
            width,
            data,
        }
    }
}

impl Schematic {
    fn find_numbers(data: &str) -> Vec<Number> {
        let pattern = Regex::new(r"\d+").unwrap();
        let numbers_on_line = |(lineno, line)| {
            pattern.find_iter(line).map(move |number| Number {
                value: number.as_str().parse().unwrap(),
                lineno,
                begin: number.start(),
                end: number.end() - 1,
            })
        };
        data.lines()
            .enumerate()
            .flat_map(numbers_on_line)
            .collect::<Vec<_>>()
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let schematic: Schematic = fs::read_to_string("input.dat")?.into();

    let is_symbol = |(x, y)| {
        let c: char = schematic.get(y, x);
        !c.is_ascii_digit() && c != '.'
    };

    let is_part_number = |number: &&Number| {
        number
            .neighborhood(schematic.width, schematic.height)
            .into_iter()
            .any(is_symbol)
    };

    let part_numbers = schematic
        .numbers
        .iter()
        .filter(is_part_number)
        .map(|&Number { value, .. }| value);

    let ans: u32 = part_numbers.sum();
    assert_eq!(ans, 553825);
    Ok(println!("{}", ans)) // 553825
}
