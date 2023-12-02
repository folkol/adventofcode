use std::fs;

fn parse_turn(turn: &str) -> [u32; 3] {
    let mut red = 0;
    let mut green = 0;
    let mut blue = 0;
    for cube_count in turn.split(',') {
        if let Some((number, color)) = cube_count.trim().split_once(' ') {
            let number: u32 = number.parse::<u32>().unwrap();
            match color {
                "red" => red = number,
                "green" => green = number,
                _ => blue = number,
            };
        }
    }
    [red, green, blue]
}

fn parse_game(line: &str) -> (u32, Vec<[u32; 3]>) {
    let (game_spec, turns) = line.split_once(':').unwrap();
    let is_garbage = |c: char| !c.is_numeric();
    let game_id: u32 = game_spec.trim_start_matches(is_garbage).parse().unwrap();
    (game_id, turns.split(';').map(parse_turn).collect())
}

fn maybe_id((game, turns): (u32, Vec<[u32; 3]>)) -> Option<u32> {
    let impossible = |[r, g, b]: [u32; 3]| r > 12 || g > 13 || b > 14;
    if turns.into_iter().any(impossible) {
        return None;
    }

    Some(game)
}

fn main() -> std::io::Result<()> {
    let ans: u32 = fs::read_to_string("input.dat")?
        .lines()
        .map(parse_game)
        .filter_map(maybe_id)
        .sum();
    println!("{}", ans);
    assert_eq!(ans, 2006);
    Ok(())
}
