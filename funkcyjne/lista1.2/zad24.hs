count5 :: Integer -> Integer -> Integer
count5 0 s = 5
count5 n 5 = count5 d (s + d) where d = div n 5