use std::collections::HashMap;

type Coord = (i64, i64, i64);

fn main() {
    let coords: Vec<_> = std::fs::read_to_string("input.dat")
        .expect("Couldn't read input file")
        .lines()
        .map(parse_coord)
        .collect();

    let mut pairs: Vec<_> = coords
        .iter()
        .enumerate()
        .flat_map(|(i, &a)| coords.iter().skip(i + 1).map(move |&b| (a, b)))
        .collect();

    pairs.sort_by_key(square_distance);

    let (mut parents, mut sizes) = coords.into_iter().map(|c| ((c, c), (c, 1))).unzip();
    for (a, b) in pairs {
        let group_a = find_group(&parents, a);
        let group_b = find_group(&parents, b);
        union(&mut parents, &mut sizes, group_a, group_b);
        if sizes.len() == 1 {
            println!("{}", a.0 * b.0);
            break;
        }
    }
}

fn parse_coord(line: &str) -> Coord {
    let [x, y, z] = line
        .split(',')
        .map_while(|s| s.parse().ok())
        .collect::<Vec<_>>()
        .try_into()
        .unwrap();
    (x, y, z)
}

fn square_distance(((x1, y1, z1), (x2, y2, z2)): &(Coord, Coord)) -> i64 {
    let dx = x2 - x1;
    let dy = y2 - y1;
    let dz = z2 - z1;
    dx * dx + dy * dy + dz * dz
}

fn union(
    parents: &mut HashMap<Coord, Coord>,
    sizes: &mut HashMap<Coord, usize>,
    root_a: Coord,
    root_b: Coord,
) {
    if root_a == root_b {
        return;
    }

    parents.insert(root_a, root_b);
    let a_size = sizes.remove(&root_a).expect("Missing size for root_a");
    *sizes.get_mut(&root_b).expect("Missing size for root_b") += a_size;
}

fn find_group(parents: &HashMap<Coord, Coord>, mut current: Coord) -> Coord {
    while let Some(&parent) = parents.get(&current) {
        if parent == current {
            break;
        }
        current = parent;
    }
    current
}
