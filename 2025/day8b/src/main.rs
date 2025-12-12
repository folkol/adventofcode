use std::collections::HashMap;

type Coord = (i64, i64, i64);

fn main() {
    let data = std::fs::read_to_string("input.dat").unwrap();
    let coords: Vec<_> = data.lines().map(parse_coord).collect();

    println!("{}", coords.len());

    let mut pairs: Vec<_> = coords
        .iter()
        .enumerate()
        .flat_map(|(i, &a)| coords.iter().skip(i + 1).map(move |&b| (a, b)))
        .collect();

    pairs.sort_by_key(distance);

    let mut parents: HashMap<Coord, Coord> = HashMap::new();
    let mut sizes: HashMap<Coord, usize> = HashMap::new();
    for coord in coords {
        parents.insert(coord, coord);
        sizes.insert(coord, 1);
    }
    for (a, b) in pairs.into_iter() {
        let group_a = find_group(&mut parents, a);
        let group_b = find_group(&mut parents, b);
        if group_a == group_b {
            continue;
        }
        union(&mut parents, &mut sizes, group_a, group_b);
        let num_circuits = sizes.values().copied().filter(|&s| s > 0).count();
        if num_circuits == 1 {
            println!("{:?}", a.0 * b.0); // 192394 is too low
            break;
        }
    }
}

fn parse_coord(line: &str) -> Coord {
    let nums: Vec<i64> = line.split(',').map(|s| s.trim().parse().unwrap()).collect();
    (nums[0], nums[1], nums[2])
}

fn distance(((x1, y1, z1), (x2, y2, z2)): &(Coord, Coord)) -> i64 {
    i64::isqrt((x2 - x1).pow(2) + (y2 - y1).pow(2) + (z2 - z1).pow(2))
}

fn union(
    parents: &mut HashMap<Coord, Coord>,
    sizes: &mut HashMap<Coord, usize>,
    a: Coord,
    b: Coord,
) {
    let a_group = find_group(parents, a);
    let b_group = find_group(parents, b);
    let new_size = sizes[&a_group] + sizes[&b_group];
    parents.insert(a_group, b_group);
    sizes.insert(b_group, new_size);
    sizes.insert(a_group, 0);
}

fn find_group(parents: &mut HashMap<Coord, Coord>, mut coord: Coord) -> Coord {
    while let Some(&parent) = parents.get(&coord)
        && parent != coord
    {
        coord = parent;
    }
    coord
}
