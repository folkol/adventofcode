uncomment :: String -> String
uncomment string =
  let replacement ',' = ' '
      replacement  c   = c
  in map replacement string

parseNumbers :: String -> [Int]
parseNumbers = map read . words . uncomment

nextDay :: Int -> [Int]
nextDay 0 = [6, 8]
nextDay n = [n - 1]

--generation :: (Int, [Int]) -> [Int]
generation 0 xs = xs
generation n xs = generation (n - 1) (concatMap nextDay xs)

main :: IO()
main = do
  indata <- getLine
  let numbers = parseNumbers indata
  print $ length $ generation 80 numbers
