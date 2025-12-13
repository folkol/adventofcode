use std::fs;

fn main() {
    let coords: Vec<_> = fs::read_to_string("input.dat")
        .expect("Couldn't read input file")
        .lines()
        .map(parse_pair)
        .collect();
    let mut ans = 0;
    for [a, b] in combinations(coords) {
        let candidate = (1 + (b[0] - a[0]).abs()) * (1 + (b[1] - a[1]).abs());
        ans = ans.max(candidate);
    }
    println!("{}", ans);
}

fn parse_pair(line: &str) -> [i64; 2] {
    line.split(',')
        .map_while(|s| s.parse().ok())
        .collect::<Vec<_>>()
        .try_into()
        .unwrap()
}

fn combinations(coords: Vec<[i64; 2]>) -> Vec<[[i64; 2]; 2]> {
    coords
        .iter()
        .enumerate()
        .flat_map(|(i, x)| coords.iter().skip(i + 1).map(|y| [x.clone(), y.clone()]))
        .collect()
}
