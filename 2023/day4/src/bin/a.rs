use std::fs;

type Card = (u32, Vec<u32>, Vec<u32>);

fn as_numbers(winners: &str) -> Vec<u32> {
    winners
        .split_whitespace()
        .filter_map(|number| number.parse().ok())
        .collect::<Vec<u32>>()
}

fn parse_card(line: &str) -> Card {
    let card_pattern = regex::Regex::new(r"^Card +(\d+): (.*) \| (.*)$").unwrap();
    let (_, [game_id, winners, yours]) = card_pattern.captures(line).unwrap().extract();
    (
        game_id.parse().unwrap(),
        as_numbers(winners),
        as_numbers(yours),
    )
}

fn main() {
    let data = fs::read_to_string("input.dat").unwrap();
    let cards: Vec<_> = data.lines().map(parse_card).collect();

    let points = |(_, winners, mine): &Card| {
        let num_hits = mine.iter().filter(|n| winners.contains(n)).count() as u32;
        if num_hits > 0 {
            u32::pow(2, num_hits - 1)
        } else {
            num_hits
        }
    };
    let ans: u32 = cards.iter().map(points).sum();
    assert_eq!(ans, 32001);
    println!("{ans}");
}
