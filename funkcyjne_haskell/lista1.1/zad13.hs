euler:: Int -> Int
euler n = length [k | k <- [1..n], gcd k n == 1]

divList:: Int -> [Int]
divList n = [k | k <- [1..n], mod n k == 0]

mySum:: Int -> Int
mySum n =  sum [euler k | k <- divList n]