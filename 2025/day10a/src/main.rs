use std::fs;

type Wiring = usize;

// Inspired by https://aoc.winslowjosiah.com/solutions/2025/day/10/
fn main() {
    let data = fs::read_to_string("input.dat").expect("Error reading input.dat");
    let mut total_presses: usize = 0;

    for line in data.lines() {
        let (indicators, buttons, _joltages) = parse_machine(line);
        let presses = find_min_presses(indicators, &buttons);
        total_presses += presses;
    }

    println!("{total_presses}");
    assert_eq!(total_presses, 538);
}

fn parse_machine(line: &str) -> (Wiring, Vec<Wiring>, Vec<i64>) {
    let parts: Vec<&str> = line.split(' ').collect();
    let raw_indicators = &parts[0];
    let raw_buttons = &parts[1..parts.len() - 1];
    let _raw_joltages = &parts[parts.len() - 1];

    let indicators: Wiring = raw_indicators
        .trim_matches(['[', ']'])
        .chars()
        .rev()
        .fold(0usize, |acc, c| (acc << 1) + usize::from(c == '#'));

    let buttons: Vec<Wiring> = raw_buttons.iter().map(parse_button).collect();
    let joltages = Vec::new();

    (indicators, buttons, joltages)
}

fn parse_button(raw_button: &&str) -> Wiring {
    raw_button
        .trim_matches(['(', ')'])
        .split(',')
        .fold(0usize, |acc, s| {
            acc | (1usize << s.parse::<usize>().expect("Expected number"))
        })
}

fn find_min_presses(indicators: usize, buttons: &[usize]) -> usize {
    for num_presses in 0.. {
        for combination in make_combinations(buttons.len(), num_presses) {
            let mut pattern = 0;
            for i in combination {
                pattern = pattern ^ buttons[i];
            }
            if pattern == indicators {
                return num_presses;
            }
        }
    }
    unreachable!();
}

fn make_combinations(n: usize, k: usize) -> Vec<Vec<usize>> {
    let mut combo: Vec<usize> = (0..k).collect();
    let mut out = Vec::new();
    loop {
        out.push(combo.clone());
        // Find the rightmost position where we can increment the value
        let i = match (0..k).rev().find(|&i| combo[i] < (n - k) + i) {
            Some(i) => i,
            None => break, // No more combinations possible
        };
        combo[i] += 1;
        for j in i + 1..k {
            combo[j] = combo[j - 1] + 1;
        }
    }
    out
}
