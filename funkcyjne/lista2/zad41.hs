remdupl :: Eq a => [a] -> [a]
remdupl = foldr f []
    where
    f x [] = [x]        --gdy akumulator jest pusty dodajemy x
    f x (y:ys) =
        if (x == y) then y:ys   --gdy elementy takie same pomijamy
        else x:y:ys             --gdy inne dodajemy element na początek listy przechowywanej przez acc