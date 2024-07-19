from py_ecc.bn128 import neg, multiply, G1, G2, pairing, G12

# f(x) = 2x^2 + 3x + 1
# Let's say I want to find the value of f(sG) where s is some scalar

# the lecture says I can take an inner product <2,3,1> by <x^2,x,1>
# let's use scalar s=3 such that we are evaluating f(3G)
# I can then take the scalar to each power to get <2,3,1> by <9G,3G,1G>
# to get 18G + 9G + 1G = 28G

# is F(3G) really the same as 28G?
result = multiply(G1, 28)
print(f'result: {result}')

