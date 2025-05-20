helperRec :: Int -> Int -> Int -> Int
helperRec n k l
    | k > n     = 0
    | l > n     = helperRec n (k + 1) 1
    | gcd k l == 1 = 1 + helperRec n k (l + 1)
    | otherwise = helperRec n k (l + 1)

helper :: Int -> Int
helper n = helperRec n 1 1

dcp :: Int -> Double
dcp n = (1 / fromIntegral (n * n)) * fromIntegral (helper n)

