helper:: Int -> Int
helper n = length [(k, l) | k <- [1..n], l <- [1..n], gcd k l ==1]

dcp:: Int -> Double
dcp n = (1 / fromIntegral (n * n)) * fromIntegral (helper n)

