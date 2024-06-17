from py_ecc.bn128 import neg, multiply, G1, G2, pairing, G12
a = 4
b = 3
c = 6
d = 2

A = multiply(G1, a)
B = multiply(G2, b)
C = multiply(G1, c)
D = multiply(G2, d)

AB = pairing(B, neg(A))
CD = pairing(D, C)

print(AB + CD)
print(AB * CD)
print(G12)
