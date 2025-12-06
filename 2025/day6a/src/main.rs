use std::fs;

fn main() {
    let data = fs::read_to_string("input.dat").expect("Unable to read file");
    let mut columns: Vec<Vec<usize>> = Vec::new();
    let mut ans = 0;
    for line in data.lines() {
        for (i, e) in line.split_whitespace().enumerate() {
            if e == "*" {
                ans += columns[i].iter().product::<usize>();
            } else if e == "+" {
                ans += columns[i].iter().sum::<usize>();
            } else {
                if i >= columns.len() {
                    columns.push(Vec::new());
                }
                columns[i].push(e.parse::<usize>().expect("expected number"));
            }
        }
    }
    println!("{}", ans);
}
