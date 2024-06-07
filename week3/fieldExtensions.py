from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq

print(f'G1: {G1}\n\n')

print(f'G2: {G2}\n\n')

print(eq(add(G1, G1), multiply(G1, 2)))
# True
print(eq(add(G2, G2), multiply(G2, 2)))
# True

print("----------\n\n")

A = multiply(G2, 5)
B = multiply(G1, 6)
# below gives us a pairing in 12-dimension group G12
print(pairing(A, B))

print("---------\n\n")

A = multiply(G2, 5)
B = multiply(G1, 6)
C = multiply(G2, 5 * 6)

print(pairing(A, B) == pairing(C, G1))

print("----------\n\n")

A = multiply(G2, 5)
B = multiply(G1, 6)
C = multiply(G1, 5 * 6) # C is now a G1 point

print(pairing(A, B) == pairing(G2, C))