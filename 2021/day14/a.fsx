let ruleParser (line:string) =
    match line.Split " -> " with
    | [| a; b |] -> a, b
    | _ -> failwith "Unexpected file format"

let stitcher acc (a,b,c) =
    match acc with
    | "" -> a + b + c
    | _ -> acc + b + c

let lines = System.IO.File.ReadLines("input.dat")
let mutable template = Seq.head <| lines
let rules = lines |> Seq.skip 2
              |> Seq.map ruleParser
              |>  dict

for i in 1..10 do
    template <- template
        |> Seq.pairwise
        |> Seq.map (fun (a,b) -> (string a), rules.Item((string a) + (string b)), (string b))
        |> Seq.fold stitcher ""

let counts = template |> Seq.countBy id |> Seq.map (fun (_, count) -> count)
let min = counts |> Seq.min
let max = counts |> Seq.max

printfn "%d" (max - min)  // 4244