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

fn parse_game(line: &str) -> Vec<[u32; 3]> {
    let (_, turns) = line.split_once(':').unwrap();
    turns.split(';').map(parse_turn).collect()
}

fn calculate_power(turns: Vec<[u32; 3]>) -> u32 {
    let elementwise_max = |acc: [u32; 3], turn: &[u32; 3]| {
        [
            acc[0].max(turn[0]),
            acc[1].max(turn[1]),
            acc[2].max(turn[2]),
        ]
    };
    let [r, g, b] = turns.iter().fold([u32::MIN; 3], elementwise_max);
    r * g * b
}

fn main() -> std::io::Result<()> {
    let ans: u32 = fs::read_to_string("input.dat")?
        .lines()
        .map(parse_game)
        .map(calculate_power)
        .sum();
    Ok(println!("{}", ans))
}
