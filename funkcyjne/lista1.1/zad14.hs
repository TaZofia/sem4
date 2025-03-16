divList:: Int -> [Int]
divList n = [k | k <- [1..(n-1)], mod n k == 0]

sumDiv:: Int -> Int
sumDiv n = sum [k | k <- divList n]

isPerfect:: Int -> Bool
isPerfect n = sumDiv n == n

main = do
    let perfectNumbers = [x | x <- [1..10000], isPerfect x]
    print perfectNumbers

--main wywołanie