
power :: Integer -> Integer -> Integer
power x y = y ^ x

p2 :: Integer -> Integer
p2 = power 4
p3 :: Integer -> Integer
p3 = power 3

main = print((p2 . p3) 2)
