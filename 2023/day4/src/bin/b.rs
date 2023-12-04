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
    let cards_and_wins: Vec<_> = cards
        .iter()
        .map(|(card_id, winners, mine)| {
            let num_wins = mine.iter().filter(|x| winners.contains(x)).count();
            (
                *card_id,
                num_wins,
            )
        })
        .collect();

    let mut queue: Vec<_> = cards_and_wins.to_vec();
    let mut final_cards = Vec::new();
    while let Some((card_id, wins)) = queue.pop() {
        let wins = wins as u32;
        final_cards.push(card_id);
        let new_cards = wins.min(cards_and_wins.len() as u32 - card_id);
        for card in card_id + 1..=card_id + new_cards {
            let x1 = cards_and_wins.iter().nth(card as usize - 1).unwrap();
            queue.push(*x1);
        }
    }

    let ans = final_cards.len();
    assert_eq!(ans, 5037841);
    dbg!(ans);
}
