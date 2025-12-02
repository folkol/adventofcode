use std::fs;

fn invalid_id(n: &usize) -> bool {
    let s = n.to_string();
    let ss = s.clone() + &s;
    ss[1..ss.len() - 1].contains(&s) // "double-string trick"
}

fn parse_range(range: &str) -> impl Iterator<Item = usize> {
    range
        .split_once('-')
        .and_then(|(b, e)| Some(b.parse().ok()?..=e.parse().ok()?))
        .into_iter()
        .flatten()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result: usize = fs::read_to_string("input.dat")?
        .split(',')
        .flat_map(parse_range)
        .filter(invalid_id)
        .sum();
    println!("result: {}", result);
    Ok(())
}
