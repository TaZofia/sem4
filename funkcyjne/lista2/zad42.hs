factorial :: Int -> Int             -- silnia dla pomocy
factorial 0 = 1
factorial x = x * factorial (x-1)

approx :: Int -> Double
approx n = foldr (\k acc -> acc + 1 / fromIntegral(factorial k)) 0 [1..n]

--k jest każdym kolejnym elementem tablicy [1..n] a w acc jest nasza suma