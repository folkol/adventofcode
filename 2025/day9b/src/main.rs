use std::fs;

const SUPER_SCIENTIFIC_THRESHOLD: i64 = 50_000;

fn main() {
    let data = fs::read_to_string("input.dat").expect("Error reading input.dat");
    let coords: Vec<(i64, i64)> = data
        .lines()
        .map(|line| {
            let nums = line
                .split(',')
                .map(|n| n.trim().parse::<i64>())
                .collect::<Result<Vec<_>, _>>()
                .expect("Failed to parse numbers");
            (nums[0], nums[1])
        })
        .collect();

    let mut area = 0;
    for fixed_corner in find_notch_vertices(&coords) {
        for opposite_corner in &coords {
            let width = 1 + i64::abs(fixed_corner.0 - opposite_corner.0);
            let height = 1 + i64::abs(fixed_corner.1 - opposite_corner.1);
            let candidate = width * height;
            if candidate > area && valid_rect(&coords, opposite_corner.clone(), fixed_corner) {
                area = candidate;
            }
        }
    }

    println!("{area}");
}

fn find_notch_vertices(coords: &[(i64, i64)]) -> [(i64, i64); 2] {
    let mut bars = Vec::new();
    for i in 0..coords.len() {
        let j = (i + 1) % coords.len(); // warp around to the beginning
        let (x1, x2) = (coords[i].0, coords[j].0);
        let width = i64::abs(x2 - x1);
        if width > SUPER_SCIENTIFIC_THRESHOLD {
            if x1 > x2 {
                bars.push(i);
            } else {
                bars.push(j);
            }
        }
    }

    [coords[bars[0]], coords[bars[1]]]
}

fn valid_rect(coords: &[(i64, i64)], (x1, y1): (i64, i64), (x2, y2): (i64, i64)) -> bool {
    let rect = [
        ((x1, y1), (x2, y1)),
        ((x2, y1), (x2, y2)),
        ((x2, y2), (x1, y2)),
        ((x1, y2), (x1, y1)),
    ];

    for rect_edge in rect {
        for i in 0..coords.len() {
            let j = (i + 1) % coords.len();
            let edge = (coords[i], coords[j]);
            if proper_intersection(edge, rect_edge) {
                return false;
            }
        }
    }

    true
}

fn proper_intersection(
    (p1, p2): ((i64, i64), (i64, i64)),
    (p3, p4): ((i64, i64), (i64, i64)),
) -> bool {
    let side_of = |(a, b): ((i64, i64), (i64, i64)), p: (i64, i64)| -> i64 {
        ((p.1 - a.1) * (b.0 - a.0) - (b.1 - a.1) * (p.0 - a.0)).signum()
    };

    // For two segments to properly cross each other (not merely touch),
    // each segment's endpoints must lie on opposite sides of the other segment.
    let s1 = side_of((p1, p2), p3); // which side of p1->p2 is p3?
    let s2 = side_of((p1, p2), p4); // which side of p1->p2 is p4?
    let t1 = side_of((p3, p4), p1); // which side of p3->p4 is p1?
    let t2 = side_of((p3, p4), p2); // which side of p3->p4 is p2?

    let opposite_sides_and_non_zero = |u: i64, v: i64| (u > 0 && v < 0) || (u < 0 && v > 0);

    opposite_sides_and_non_zero(s1, s2) && opposite_sides_and_non_zero(t1, t2)
}
