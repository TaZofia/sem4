tails' :: ([Int], [[Int]]) -> [[Int]]
tails' ([], a) = [] : a
tails' (x : xs, a) = tails' (xs, [x:xs] : 0)

-- nie skończone