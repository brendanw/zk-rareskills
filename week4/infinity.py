from py_ecc.bn128 import neg, add, multiply, G1, G2, pairing, G12, is_inf

A = multiply(G1, 5)
B = multiply(G2, 6)
C = multiply(G1, 30)

AB = pairing(B, A)
C = pairing(G2, C)
print(f'C: {C}')
negC = neg(C)
print(negC)

# print(pairing(B, A))
# print(pairing(G2, C))
# print(AB * negC)
