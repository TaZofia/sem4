countEven :: [Int] -> Int
countEven = foldr (\x acc -> if even x then acc + 1 else acc) 0