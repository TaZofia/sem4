inits' :: [a] -> [[a]]
inits' [] = [[]]
inits' xs = inits' (init xs) ++ [xs]

-- nie skończone