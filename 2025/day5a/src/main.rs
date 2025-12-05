use std::ops::RangeInclusive;

fn line_to_range(line: &str) -> RangeInclusive<usize> {
    line.split_once('-')
        .and_then(|(start, end)| Some(start.parse().ok()?..=end.parse().ok()?))
        .unwrap_or(0..=0)
}

fn main() {
    let data = std::fs::read_to_string("input.dat").expect("Failed to read input file");
    let (database, ingredients) = data.split_once("\n\n").expect("Failed to split input file");
    let ranges = database.lines().map(line_to_range).collect::<Vec<_>>();

    let num_fresh = ingredients
        .lines()
        .map_while(|line| line.parse::<usize>().ok())
        .filter(|&i| ranges.iter().any(|r| r.contains(&i)))
        .count();
    println!("{num_fresh}");
}
