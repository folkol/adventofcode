use std::collections::{HashMap, HashSet, VecDeque};

type Pos = (i64, i64);
type Colony = [Amphipod; 16];


#[derive(Clone, Eq, Hash, PartialEq)]
struct Amphipod {
    n: i64,
    kind: char,
    pos: Pos,
}


fn main() {
    let amphipods = [
        Amphipod { n: 0, kind: 'B', pos: (2, 3) },
        Amphipod { n: 1, kind: 'B', pos: (2, 5) },
        Amphipod { n: 2, kind: 'C', pos: (2, 7) },
        Amphipod { n: 3, kind: 'D', pos: (2, 9) },
        Amphipod { n: 4, kind: 'D', pos: (3, 3) },
        Amphipod { n: 5, kind: 'C', pos: (3, 5) },
        Amphipod { n: 6, kind: 'B', pos: (3, 7) },
        Amphipod { n: 7, kind: 'A', pos: (3, 9) },
        Amphipod { n: 8, kind: 'D', pos: (4, 3) },
        Amphipod { n: 9, kind: 'B', pos: (4, 5) },
        Amphipod { n: 10, kind: 'A', pos: (4, 7) },
        Amphipod { n: 11, kind: 'C', pos: (4, 9) },
        Amphipod { n: 12, kind: 'D', pos: (5, 3) },
        Amphipod { n: 13, kind: 'C', pos: (5, 5) },
        Amphipod { n: 14, kind: 'A', pos: (5, 7) },
        Amphipod { n: 15, kind: 'A', pos: (5, 9) },
    ];

    println!("{}", solve(amphipods, 0, &mut HashMap::new(), i64::MAX));
}

fn solve(amphipods: Colony, total_cost: i64, memo: &mut HashMap<Colony, i64>, min_cost: i64) -> i64 {
    let game_complete = amphipods.iter().all(at_destination);
    if game_complete {
        return total_cost.min(min_cost);
    }

    if let Some(best_seen) = memo.get(&amphipods) {
        if *best_seen <= total_cost {
            return min_cost;
        }
    }
    memo.insert(amphipods.clone(), total_cost);

    let mut next_min_cost = min_cost;
    for amphipod in &amphipods {
        for pos in valid_moves(amphipod, &amphipods) {
            let mut next_state = amphipods.clone();
            if let Some(i) = next_state.iter().position(|a| a.n == amphipod.n) {
                next_state[i] = Amphipod { n: amphipod.n, kind: amphipod.kind, pos };
            }
            let cost = travel_cost(&amphipod, pos);
            let candidate = solve(next_state, total_cost + cost, memo, next_min_cost);
            next_min_cost = next_min_cost.min(candidate)
        }
    }
    return next_min_cost;
}

fn travel_cost(amphipod: &Amphipod, pos: Pos) -> i64 {
    let mut cur = amphipod.pos;
    let mut dist = 0;
    if !at_destination(amphipod) {
        dist += (cur.0 - 1).abs();
        cur.0 = 1;
    }
    dist += (cur.1 - pos.1).abs();
    dist += (cur.0 - pos.0).abs();
    dist * match amphipod.kind {
        'A' => 1,
        'B' => 10,
        'C' => 100,
        'D' => 1000,
        _ => panic!("Unexpected kind")
    }
}

fn reachable_squares(amphipod: &Amphipod, amphipods: &Colony) -> Vec<Pos> {
    fn available(pos: &Pos, amphipods: &Colony) -> bool {
        let open_space = in_hallway(pos) || in_a_room(pos);
        let occupied = amphipods.iter().any(|a| a.pos == *pos);
        open_space && !occupied
    }

    fn adjacent(pos: Pos) -> Vec<Pos> {
        vec![
            (pos.0 - 1, pos.1),
            (pos.0 + 1, pos.1),
            (pos.0, pos.1 - 1),
            (pos.0, pos.1 + 1),
        ]
    }

    let mut result: Vec<Pos> = vec![];
    let mut visited: HashSet<Pos> = HashSet::new();
    let mut queue: VecDeque<Pos> = VecDeque::from(vec![amphipod.pos]);
    while let Some(pos) = queue.pop_front() {
        result.push(pos);
        for neighbour in adjacent(pos) {
            if available(&neighbour, amphipods) && !visited.contains(&neighbour) {
                queue.push_back(neighbour);
                visited.insert(neighbour);
            }
        }
    }
    result
}

fn room_for(amphipod: &Amphipod) -> [(i64, i64); 4] {
    return match amphipod.kind {
        'A' => [(5, 3), (4, 3), (3, 3), (2, 3)],
        'B' => [(5, 5), (4, 5), (3, 5), (2, 5)],
        'C' => [(5, 7), (4, 7), (3, 7), (2, 7)],
        'D' => [(5, 9), (4, 9), (3, 9), (2, 9)],
        _ => panic!("Unexpected kind")
    };
}

fn valid_moves(amphipod: &Amphipod, amphipods: &Colony) -> Vec<Pos> {
    fn by_the_door(pos: &Pos) -> bool {
        [(1, 3), (1, 5), (1, 7), (1, 9)].contains(pos)
    }

    fn mixed_room(amphipod: &Amphipod, amphipods: &Colony) -> bool {
        let room = room_for(amphipod);
        let in_room = |a: &&Amphipod| room.contains(&a.pos);
        amphipods.iter().filter(in_room).any(|a| a.kind != amphipod.kind)
    }

    let mut ans = vec![amphipod.pos];
    let squares = reachable_squares(amphipod, amphipods);

    if in_hallway(&amphipod.pos) {
        if !mixed_room(amphipod, amphipods) {
            let in_squares = |pos: &&Pos| squares.contains(pos);
            if let Some(pos) = room_for(amphipod).iter().find(in_squares) {
                ans.push(*pos)
            }
        }
    } else if mixed_room(amphipod, amphipods) || !at_destination(amphipod) {
        let out_of_the_way = |s: &&Pos| in_hallway(s) && !by_the_door(s);
        ans.extend(squares.iter().filter(out_of_the_way));
    }

    ans
}

fn in_a_room(pos: &Pos) -> bool {
    pos.0 > 1 && pos.0 <= 5 && [3, 5, 7, 9].contains(&pos.1)
}


fn in_hallway(pos: &Pos) -> bool {
    pos.1 >= 1 && pos.1 <= 11 && pos.0 == 1
}

fn at_destination(amphipod: &Amphipod) -> bool {
    room_for(amphipod).contains(&amphipod.pos)
}
