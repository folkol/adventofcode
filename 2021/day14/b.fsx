let ruleParser (line:string) =
    match line.Split " -> " with
    | [| a; b |] -> [a[0];a[1]], (char b)
    | _ -> failwith "Unexpected file format"

let lines = System.IO.File.ReadLines("input.dat")
let template = Seq.head <| lines
let rules = lines |> Seq.skip 2
              |> Seq.map ruleParser
              |>  dict

let insert ((a, b), c) =
    let ins = rules.[[a;b]]
    [((a, ins), c); ((ins, b), c);]

let insertedCharCounts ((a, b), c) =
    let ins = rules.[[a;b]]
    (ins, c)

let rec pairInsertions (step:int) (charCounts:seq<char*int64>) (pairCounts:seq<(char*char)*int64>) =
    if step > 0 then
        let counts' =
            pairCounts
            |> Seq.map insert
            |> Seq.concat
            |> Seq.groupBy fst
            |> Seq.map (fun (k, lst) -> k, lst |> Seq.sumBy snd)
        let insertCharCounts =
            pairCounts
            |> Seq.map insertedCharCounts
        let charCounts' =
            [charCounts; insertCharCounts]
            |> Seq.concat
            |> Seq.groupBy fst
            |> Seq.map (fun (k, lst) -> k, lst |> Seq.sumBy snd)
        pairInsertions (step - 1) charCounts' counts'
    else charCounts

let charCounts:seq<char * int64> =
    template
    |> Seq.countBy id
    |> Seq.map (fun (k, v) -> k, (v|>int64))
let pairCounts:seq<(char*char)*int64> =
    template
    |> Seq.pairwise
    |> Seq.countBy id
    |> Seq.map (fun (k, v) -> k, (v|>int64))

let finalCounts = pairInsertions 40 charCounts pairCounts
let min = finalCounts |> Seq.map snd |> Seq.min
let max = finalCounts |> Seq.map snd |> Seq.max
printfn "ans: %d" (max - min)