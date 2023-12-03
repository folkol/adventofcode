use std::error::Error;
use std::fs;

fn main() -> Result<(), Box<dyn Error>> {
    let data = fs::read_to_string("input.dat")?;
    let lines: Vec<(usize, Vec<char>)> = data
        .lines()
        .map(|line| line.chars().collect())
        .enumerate()
        .collect();
    let mut numbers: Vec<_> = Vec::new();
    let mut part_numbers = Vec::new();
    for (mut i, line) in &lines {
        let mut begin = 0;
        let mut end = 0;
        let mut inside: bool = false;
        for (j, c) in line.iter().enumerate() {
            if c.is_ascii_digit() && !inside {
                inside = true;
                begin = j;
                end = begin;
            }
            if c.is_ascii_digit() {
                end = j;
            }
            if !c.is_ascii_digit() && inside {
                numbers.push((i, begin, end, line.len()));
                inside = false;
            }
        }
        if inside {
            numbers.push((i, begin, end, line.len()));
        }
        println!("{i:03}: {line:?}");
        part_numbers.push(1)
    }

    let mut part_numbers: Vec<u32> = Vec::new();
    'outer: for &(line, begin, end, llen) in &numbers {
        let above = if line > 0 {
            line - 1
        } else {
            line
        };
        let below = if line < lines.len() - 2 {
            line + 1
        } else {
            line
        };
        let left = if begin > 0 {
            begin - 1
        } else {
            begin
        };
        let right = if end < llen - 2 {
            end + 1
        } else {
            end
        };
        for row in above..=below {
            for col in left..=right {
                let c = lines[row].1[col];
                if !c.is_ascii_digit() && c != '.' {
                    let mut tmp = String::new();
                    for n in begin..=end {
                        tmp.push(lines[line].1[n]);
                    }
                    println!("Inspecting '{c}' @ ({row}, {col}), found symbol, adding {tmp}");
                    part_numbers.push(tmp.parse()?);
                    continue 'outer;
                }
            }
        }
    }

    let i1 = part_numbers.iter().sum::<u32>();
    dbg!(i1);

    assert_eq!(i1, 553825);

    Ok(())
}
