divList:: Int -> [Int]
divList n = [k | k <- [1..(n-1)], mod n k == 0]

sumDiv:: Int -> Int
sumDiv n = sum (divList n)

areFriends:: Int -> Int -> Bool
areFriends m n = (m /= n) && (sumDiv n == m) && (sumDiv m == n)

pairs:: Int -> [(Int, Int)]
pairs k = [(m, n) | m <- [1..k], let n = sumDiv m, m < n, sumDiv n == m ]

main = do
    let friendPairs = pairs 100000
    print friendPairs