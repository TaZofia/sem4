select :: [a] -> [(a, [a])]
select [] = []
select (y : ys) = (y, ys) : [(z, y : zs) | (z, zs) <- select ys]

permutations' :: [a] -> [[a]]
permutations' [] = [[]]
permutations' xs = [x : ys | (x , rest) <- select xs, ys <- permutations' rest]

--nie działa