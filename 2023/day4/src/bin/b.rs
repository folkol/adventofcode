use std::fs;

type Card = (usize, Vec<u32>, Vec<u32>);

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
    let card_and_copies = |card: &Card| {
        let (card_id, winners, mine) = card;
        let num_wins = mine.iter().filter(|n| winners.contains(n)).count();
        (*card_id, num_wins)
    };
    let cards_with_copies: Vec<_> = cards
        .iter()
        .map(card_and_copies)
        .collect();

    let mut queue: Vec<_> = cards_with_copies.to_vec();
    let mut ans = 0;
    while let Some((card_id, wins)) = queue.pop() {
        queue.extend(cards_with_copies.iter().skip(card_id).take(wins));
        ans += 1;
    }
    assert_eq!(ans, 5037841);
    println!("{ans}");
}
