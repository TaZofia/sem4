import Data.List

--Wersja dla leniwych
splits' :: [a] -> [([a], [a])]
splits' xs = zip (inits xs)(tails xs)

--Wersja pro
splitspro :: [a] -> [([a], [a])]
splitspro [] = [([], [])]
splitspro (x : xs) = ([], x : xs) : (map(\(a,b) -> (x:a,b))(splitspro xs))