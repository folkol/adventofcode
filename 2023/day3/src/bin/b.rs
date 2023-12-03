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
    fn neighborhood(&self, width: usize, height: usize) -> Vec<(u32, u32)> {
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

    fn adjacent(&self, square: (usize, usize), width: usize, height: usize) -> bool {
        let row = square.0 as u32;
        let col = square.1 as u32;
        self.neighborhood(width, height).contains(&(row, col))
    }
}

struct Schematic {
    numbers: Vec<Number>,
    width: usize,
    height: usize,
    data: String,
}

impl Schematic {
    fn stars(&self) -> Vec<(usize, usize)> {
        let mut stars = Vec::new();
        for (row, line) in self.data.lines().enumerate() {
            for (col, c) in line.chars().enumerate() {
                if c == '*' {
                    stars.push((row, col))
                }
            }
        }
        stars
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

    let mut gear_ratios: Vec<u32> = Vec::new();
    for star in schematic.stars() {
        let adjacent_part_numbers: Vec<_> = schematic
            .numbers
            .iter()
            .filter(|number| number.adjacent(star, schematic.width, schematic.height))
            .map(|Number { value, .. }| value)
            .collect();
        if adjacent_part_numbers.len() == 2 {
            gear_ratios.push(adjacent_part_numbers.into_iter().product());
        }
    }

    let ans: u32 = gear_ratios.iter().sum();
    assert_eq!(ans, 93994191);
    Ok(println!("{}", ans)) // 553825
}
