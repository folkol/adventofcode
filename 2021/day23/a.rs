use std::borrow::{Borrow, BorrowMut};
use std::collections::{HashMap, HashSet, VecDeque};
use std::process;

type Pos = (i64, i64);

#[derive(Clone)]
struct Amphipod {
    n: i64,
    kind: char,
    pos: Pos,
}

type GameState = ((i64, Pos), (i64, Pos), (i64, Pos), (i64, Pos), (i64, Pos), (i64, Pos), (i64, Pos), (i64, Pos));

static mut min_cost: f64 = f64::INFINITY;

fn main() {
    let mut previous_states: HashMap<GameState, i64> = HashMap::new();
    // # #D#C#B#A#
    // # #D#B#A#C#
    // let amphipods = [
    //     Amphipod { n: 0, kind: 'A', pos: (3, 3) },
    //     Amphipod { n: 1, kind: 'A', pos: (3, 9) },
    //     Amphipod { n: 2, kind: 'B', pos: (2, 3) },
    //     Amphipod { n: 3, kind: 'B', pos: (2, 7) },
    //     Amphipod { n: 4, kind: 'C', pos: (2, 5) },
    //     Amphipod { n: 5, kind: 'C', pos: (3, 7) },
    //     Amphipod { n: 6, kind: 'D', pos: (2, 9) },
    //     Amphipod { n: 7, kind: 'D', pos: (3, 5) },
    // ];

    let amphipods = [
        Amphipod { n: 0, kind: 'A', pos: (3, 7) },
        Amphipod { n: 1, kind: 'A', pos: (3, 9) },
        Amphipod { n: 2, kind: 'B', pos: (2, 3) },
        Amphipod { n: 3, kind: 'B', pos: (2, 5) },
        Amphipod { n: 4, kind: 'C', pos: (2, 7) },
        Amphipod { n: 5, kind: 'C', pos: (3, 5) },
        Amphipod { n: 6, kind: 'D', pos: (2, 9) },
        Amphipod { n: 7, kind: 'D', pos: (3, 3) },
    ];

    // print_board(amphipods, '')
    unsafe { solve(amphipods, 0, &mut previous_states); }
    // # assert min_cost == 15111, min_cost
    // assert min_cost == 12521, min_cost
    unsafe { println!("min_cost: {}", min_cost); }
}

unsafe fn solve(mut amphipods: [Amphipod; 8], cost: i64, previous_states: &mut HashMap<GameState, i64>) {
    if all_done(&amphipods) {
        if cost < min_cost as i64 {
            min_cost = cost as f64;
            println!("Found new min {}", min_cost);
            println!("{:?}", state_for(&amphipods));
        }
        return;
    }
    // TODO unwrap_or...
    // let i = 99999;
    // let prev_cost = match previous_states.get(&state_for(&amphipods)) {
    //     Some(n) => n,
    //     None => &i
    // };
    let prev_cost = previous_states.get(&state_for(&amphipods)).unwrap_or(i64::MAX.borrow());
    if cost < *prev_cost {
        previous_states.insert(state_for(&amphipods), cost);
    } else {
        return;
    }
    let mut moved = false;
    for amphipod in amphipods.iter() {
        let mut moves = valid_moves(&amphipod, &amphipods);
        moves.sort();
        // println!("{:?}", moves);
        for pos in moves {
            moved = true;
            let mut next_state = amphipods.clone();
            let idx = next_state.iter().position(|a| a.n == amphipod.n).unwrap();
            next_state[idx] = Amphipod { n: amphipod.n, kind: amphipod.kind, pos: pos };
            let delta = travel_cost(&amphipod, pos, &amphipods);
            // println!("{:?} {:?} {}", amphipod.pos, pos, delta);
            solve(next_state, cost + delta, previous_states);
        }
    }
    if !moved {
        println!("Game over");
        process::exit(0);
    }
}

fn travel_cost(amphipod: &Amphipod, pos: Pos, amphipods: &[Amphipod; 8]) -> i64 {

    // cost_for = {
    //     'A': 1,
    //     'B': 10,
    //     'C': 100,
    //     'D': 1000,
    // }
    //
    // cur = list(amphipod.pos)
    // travelled = 0

    let mut cur = amphipod.pos;
    let mut travelled = 0;
    if in_rooms(cur) && cur.1 != pos.1 {
        travelled += (cur.0 - 1).abs();
        cur.0 = 1;
    }
    travelled += (cur.1 - pos.1).abs();
    travelled += (cur.0 - pos.0).abs();
    travelled * match amphipod.kind {
        'A' => 1,
        'B' => 10,
        'C' => 100,
        'D' => 1000,
        _ => panic!("Unexpected kind")
    }
}

fn in_rooms(pos: Pos) -> bool {
    let rooms = [
        (2, 3), (3, 3),
        (2, 5), (3, 5),
        (2, 7), (3, 7),
        (2, 9), (3, 9)];

    rooms.contains(&pos)
}

fn valid_moves(amphipod: &Amphipod, amphipods: &[Amphipod; 8]) -> Vec<Pos> {
    let mut ans = vec![];
    ans.push(amphipod.pos);

    let mut reachable_squares = bfs(amphipod, amphipods);

    if in_hallway(amphipod.pos) {
        let [dest_hi, dest_lo] = room_for(amphipod);
        if reachable_squares.contains(&dest_lo) {
            ans.push(dest_lo);
        } else if reachable_squares.contains(&dest_hi) {
            let occupant = amphipod_at(dest_lo, amphipods);
            if occupant.is_some() && occupant.unwrap().kind == amphipod.kind { // TODO Can this be none?
                ans.push(dest_hi);
            }
        }
    } else if room_for(amphipod).contains(&amphipod.pos) {
        if mixed(amphipod, amphipods) {
            reachable_squares.iter_mut().filter(|pos| in_hallway(**pos) && !in_atria(pos)).for_each(|p| ans.push(*p));
        }
    } else {  // In wrong room
        let [dest_hi, dest_lo] = room_for(amphipod);
        if reachable_squares.contains(&dest_lo) {
            ans.push(dest_lo);
        } else if reachable_squares.contains(&dest_hi) {
            let occupant = amphipod_at(dest_lo, amphipods);
            if occupant.is_some() && occupant.unwrap().kind == amphipod.kind { // TODO Can this be none?
                ans.push(dest_hi);
            }
        } else {
            reachable_squares.iter_mut().filter(|pos| in_hallway(**pos) && !in_atria(pos)).for_each(|p| ans.push(*p));
        }
    }

    ans
}

fn in_atria(pos: &&mut Pos) -> bool {
    let atria = [(1, 3), (1, 5), (1, 7), (1, 9)];
    atria.contains(&pos)
}

fn mixed(amphipod: &Amphipod, amphipods: &[Amphipod; 8]) -> bool {
    let room = room_for(amphipod);
    amphipods.iter().filter(|a| room.contains(&a.pos)).any(|a| a.kind != amphipod.kind)
}

fn amphipod_at(pos: Pos, amphipods: &[Amphipod; 8]) -> Option<&Amphipod> {
    amphipods.iter().find(|a| a.pos == pos)
}

fn in_hallway(pos: Pos) -> bool {
    pos.0 == 1
}

fn bfs(amphipod: &Amphipod, amphipods: &[Amphipod; 8]) -> Vec<Pos> {
    let mut visited: HashSet<Pos> = HashSet::new();
    let mut reachable_squares: Vec<Pos> = vec![];
    let mut queue: VecDeque<Pos> = VecDeque::new();
    queue.push_back(amphipod.pos);
    while !queue.is_empty() {
        let pos = queue.pop_front().unwrap();
        reachable_squares.push(pos);
        for neighbour in neighbours(pos) {
            if open_space(neighbour) && !occupied(neighbour, amphipods) && !visited.contains(&neighbour) {
                queue.push_back(neighbour);
                visited.insert(neighbour);
            }
        }
    }
    reachable_squares
}

fn occupied(pos: Pos, amphipods: &[Amphipod; 8]) -> bool {
    amphipods.iter().any(|a| a.pos == pos)
}

fn open_space(pos: Pos) -> bool {
    // HALLWAY = set((1, j) for j in range(1, 12))
    // ATRIA = {(1, 3), (1, 5), (1, 7), (1, 9)}
    // ROOM1 = [(2, 3), (3, 3)]
    // ROOM2 = [(2, 5), (3, 5)]
    // ROOM3 = [(2, 7), (3, 7)]
    // ROOM4 = [(2, 9), (3, 9)]
    // ROOMS = {*ROOM1, *ROOM2, *ROOM3, *ROOM4}
    // pos = row, col
    // return pos in HALLWAY or pos in ROOMS

    let open_squares: Vec<Pos> = vec![
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (1, 8),
        (1, 9),
        (1, 10),
        (1, 11),
        (2, 3),
        (3, 3),
        (2, 5),
        (3, 5),
        (2, 7),
        (3, 7),
        (2, 9),
        (3, 9),
    ];
    open_squares.contains(&pos)
}

fn neighbours(pos: Pos) -> Vec<Pos> {
    vec![
        (pos.0 - 1, pos.1),
        (pos.0 + 1, pos.1),
        (pos.0, pos.1 - 1),
        (pos.0, pos.1 + 1),
    ]
}

fn all_done(amphipods: &[Amphipod; 8]) -> bool {
    // todo!()
    // def all_done(amphipods):
    // return all(a.pos in room_for(a) for a in amphipods)

    amphipods.iter().all(|a| room_for(a).contains(&a.pos))
}

fn room_for(amphipod: &Amphipod) -> [(i64, i64); 2] {
    let room1 = [(2, 3), (3, 3)];
    let room2 = [(2, 5), (3, 5)];
    let room3 = [(2, 7), (3, 7)];
    let room4 = [(2, 9), (3, 9)];

    return match amphipod.kind {
        'A' => room1,
        'B' => room2,
        'C' => room3,
        'D' => room4,
        _ => panic!("Unexpected kind")
    };
}

// Actually needed? We might be able to index map with Array?
fn state_for(amphipods: &[Amphipod; 8]) -> GameState {
    (
        (amphipods[0].n, amphipods[0].pos),
        (amphipods[1].n, amphipods[1].pos),
        (amphipods[2].n, amphipods[2].pos),
        (amphipods[3].n, amphipods[3].pos),
        (amphipods[4].n, amphipods[4].pos),
        (amphipods[5].n, amphipods[5].pos),
        (amphipods[6].n, amphipods[6].pos),
        (amphipods[7].n, amphipods[7].pos),
    )
}

/*
class Amphipod:
    def __init__(self, n, kind, row, col):
        self.n = n
        self.kind = kind
        self.col = col
        self.row = row
        self.pos = (row, col)

    def __str__(self) -> str:
        return f'Amphipod({self.n}, {self.row}, {self.col})'


def print_board(amphipods, indent):
    board = [
        "#############",
        "#...........#",
        "###.#.#.#.###",
        "  #.#.#.#.#  ",
        "  #########  ",
    ]
    for row, line in enumerate(board):
        print(indent, end='')
        for col, c in enumerate(line):
            pos = (row, col)
            output = next((
                a.kind
                for a in amphipods
                if a.pos == pos
            ), c)
            print(output, sep='', end='')
        print()


def open_space(row, col):
    HALLWAY = set((1, j) for j in range(1, 12))
    ATRIA = {(1, 3), (1, 5), (1, 7), (1, 9)}
    ROOM1 = [(2, 3), (3, 3)]
    ROOM2 = [(2, 5), (3, 5)]
    ROOM3 = [(2, 7), (3, 7)]
    ROOM4 = [(2, 9), (3, 9)]
    ROOMS = {*ROOM1, *ROOM2, *ROOM3, *ROOM4}

    pos = row, col
    return pos in HALLWAY or pos in ROOMS


def occupied(pos, amphipods):
    return any(a for a in amphipods if pos == a.pos)


def room_for(amphipod):
    HALLWAY = set((1, j) for j in range(1, 12))
    ATRIA = {(1, 3), (1, 5), (1, 7), (1, 9)}
    ROOM1 = [(2, 3), (3, 3)]
    ROOM2 = [(2, 5), (3, 5)]
    ROOM3 = [(2, 7), (3, 7)]
    ROOM4 = [(2, 9), (3, 9)]
    ROOMS = {*ROOM1, *ROOM2, *ROOM3, *ROOM4}

    destinations = {
        'A': ROOM1,
        'B': ROOM2,
        'C': ROOM3,
        'D': ROOM4,
    }
    return destinations[amphipod.kind]


def neighbours(row, col):
    yield row - 1, col
    yield row + 1, col
    yield row, col - 1
    yield row, col + 1


def bfs(amphipod, amphipods):
    visited = set()
    queue = deque()
    queue.append(amphipod.pos)
    while queue:
        pos = queue.pop()
        yield pos
        for neighbour in neighbours(*pos):
            if open_space(*neighbour) \
                    and not occupied(neighbour, amphipods) \
                    and neighbour not in visited:
                # yield neighbour
                queue.append(neighbour)
                visited.add(neighbour)


def amphipod_at(pos, amphipods):
    return next((a for a in amphipods if a.pos == pos), None)


def mixed(amphipod, amphipods):
    room = room_for(amphipod)
    bools = [a.kind != amphipod.kind for a in amphipods if a.pos in room]
    return any(bools)


def in_hallway(pos):
    HALLWAY = set((1, j) for j in range(1, 12))
    ATRIA = {(1, 3), (1, 5), (1, 7), (1, 9)}
    ROOM1 = [(2, 3), (3, 3)]
    ROOM2 = [(2, 5), (3, 5)]
    ROOM3 = [(2, 7), (3, 7)]
    ROOM4 = [(2, 9), (3, 9)]
    ROOMS = {*ROOM1, *ROOM2, *ROOM3, *ROOM4}
    return pos in HALLWAY


def in_atria(s):
    HALLWAY = set((1, j) for j in range(1, 12))
    ATRIA = {(1, 3), (1, 5), (1, 7), (1, 9)}
    ROOM1 = [(2, 3), (3, 3)]
    ROOM2 = [(2, 5), (3, 5)]
    ROOM3 = [(2, 7), (3, 7)]
    ROOM4 = [(2, 9), (3, 9)]
    ROOMS = {*ROOM1, *ROOM2, *ROOM3, *ROOM4}
    return s in ATRIA


def valid_moves(amphipod, amphipods):
    yield amphipod.pos
    reachable_squares = list(bfs(amphipod, amphipods))

    if in_hallway(amphipod.pos):
        dest_hi, dest_lo = room_for(amphipod)
        if dest_lo in reachable_squares:
            yield dest_lo
        elif dest_hi in reachable_squares:
            occupant = amphipod_at(dest_lo, amphipods)
            if occupant.kind == amphipod.kind:
                yield dest_hi
    elif amphipod.pos in room_for(amphipod):
        if mixed(amphipod, amphipods):
            yield from (
                s
                for s in reachable_squares
                if in_hallway(s) and not in_atria(s)
            )
    else:  # in wrong room
        dest_hi, dest_lo = room_for(amphipod)
        if dest_lo in reachable_squares:
            yield dest_lo
        elif dest_hi in reachable_squares:
            occupant = amphipod_at(dest_lo, amphipods)
            if occupant.kind == amphipod.kind:
                yield dest_hi
        else:
            yield from (
                s
                for s in reachable_squares
                if in_hallway(s) and not in_atria(s)
            )


previous_states = {}


def all_done(amphipods):
    return all(a.pos in room_for(a) for a in amphipods)


def in_rooms(param):
    HALLWAY = set((1, j) for j in range(1, 12))
    ATRIA = {(1, 3), (1, 5), (1, 7), (1, 9)}
    ROOM1 = [(2, 3), (3, 3)]
    ROOM2 = [(2, 5), (3, 5)]
    ROOM3 = [(2, 7), (3, 7)]
    ROOM4 = [(2, 9), (3, 9)]
    ROOMS = {*ROOM1, *ROOM2, *ROOM3, *ROOM4}
    return param in ROOMS


def travel_cost(amphipod, pos, amphipods):
    cost_for = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000,
    }

    cur = list(amphipod.pos)
    travelled = 0
    if in_rooms(tuple(cur)) and cur[1] != pos[1]:
        travelled += abs(cur[0] - 1)
        cur[0] = 1
    travelled += abs(cur[1] - pos[1])
    travelled += abs(cur[0] - pos[0])

    return cost_for[amphipod.kind] * travelled


min_cost = math.inf


def solve(amphipods, cost=0, indent=''):
    global min_cost
    if all_done(amphipods):
        if cost < min_cost:
            min_cost = cost
            print('Found new min', min_cost)
        return
    if cost < previous_states.get(state_for(amphipods), math.inf):
        previous_states[state_for(amphipods)] = cost
    else:
        return
    moved = False
    for amphipod in amphipods:
        moves = list(valid_moves(amphipod, amphipods))
        for pos in moves:
            moved = True
            next_state = [
                a if a.n != amphipod.n else Amphipod(a.n, a.kind, *pos)
                for a in amphipods
            ]
            delta = travel_cost(amphipod, pos, amphipods)
            solve(next_state, cost=cost + delta, indent=indent + '  ')
    if not moved:
        print('Game over')
        sys.exit()


def state_for(next_state):
    return tuple((a.n, a.row, a.col) for a in next_state)


def main():
    # #D#C#B#A#
    # #D#B#A#C#
    amphipods = [
        Amphipod(0, 'A', 3, 3),
        Amphipod(1, 'A', 3, 9),
        Amphipod(2, 'B', 2, 3),
        Amphipod(3, 'B', 2, 7),
        Amphipod(4, 'C', 2, 5),
        Amphipod(5, 'C', 3, 7),
        Amphipod(6, 'D', 2, 9),
        Amphipod(7, 'D', 3, 5),
    ]
    # amphipods = [
    #     Amphipod(0, 'A', 3, 7),
    #     Amphipod(1, 'A', 3, 9),
    #     Amphipod(2, 'B', 2, 3),
    #     Amphipod(3, 'B', 2, 5),
    #     Amphipod(4, 'C', 2, 7),
    #     Amphipod(5, 'C', 3, 5),
    #     Amphipod(6, 'D', 2, 9),
    #     Amphipod(7, 'D', 3, 3),
    # ]
    print_board(amphipods, '')
    solve(amphipods, cost=0)
    # assert min_cost == 15111, min_cost
    assert min_cost == 12521, min_cost
    print(min_cost)


if __name__ == '__main__':
    main()
*/