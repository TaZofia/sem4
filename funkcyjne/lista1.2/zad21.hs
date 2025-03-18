partition :: (a -> Bool) -> [a] -> ([a], [a]) -> ([a], [a])

addfst :: a -> ([a], [a]) -> ([a], [a])
addfst x pair = (x fst (pair) , snd (pair))

addsnd :: a -> ([a], [a]) -> ([a], [a])
addsnd x pair = fst (pair), x : snd (pair)


--nie skończone