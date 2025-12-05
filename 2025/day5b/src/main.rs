use std::ops::RangeInclusive;
use std::vec::IntoIter;

fn main() {
    let data = std::fs::read_to_string("input.dat").expect("Failed to read input file");
    let (database, _) = data.split_once("\n\n").expect("Failed to split input file");
    let mut ranges = database.lines().map(line_to_range).collect::<Vec<_>>();
    ranges.sort_by_key(|range| *range.start());

    let ans = merge_ranges(ranges.into_iter())
        .into_iter()
        .map(|range| range.end() - range.start() + 1)
        .sum::<usize>();
    println!("{}", ans);
}

fn line_to_range(line: &str) -> RangeInclusive<usize> {
    line.split_once('-')
        .and_then(|(start, end)| Some(start.parse().ok()?..=end.parse().ok()?))
        .unwrap_or(0..=0)
}

fn merge_ranges(mut ranges: IntoIter<RangeInclusive<usize>>) -> Vec<RangeInclusive<usize>> {
    let mut merged = vec![ranges.next().unwrap_or(0..=0)];

    for range in ranges {
        let current = merged.last_mut().expect("No ranges to merge");
        if *range.start() <= *current.end() {
            let start = *current.start();
            let new_end = usize::max(*current.end(), *range.end());
            *current = start..=new_end;
        } else {
            merged.push(range);
        }
    }

    merged
}
