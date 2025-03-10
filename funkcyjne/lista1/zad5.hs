f = \x -> 1 + x * (x + 1)
g = \x y -> x + y ^ 2
h = \y x -> x + y ^ 2

main = do
    print(f 1)     --3
    print(g 1 2)   --5
    print(h 1 2)   --3