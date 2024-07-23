from py_ecc.bn128 import neg, add, multiply, G1, G2, pairing, G12, is_inf, eq

A = multiply(G2, 25)
B = multiply(G1, 4)
C = multiply(G2, 20)
D = multiply(G1, 2)
P = multiply(G2, 15)
Q = multiply(G1, 4)

# 25 * 4 == 20 * 2 + 15 * 4
AB = pairing(A, B)
CD = pairing(C, D)
PQ = pairing(P, Q)

# below check does not work
if not eq(AB, CD + PQ):
    print("addition does not work for comparing G12 points")

# below check does work
if eq (AB, CD * PQ):
    print("multiplication does work for comparing G12 points")

# if ab = cd + pq, then it must be the case that
# e^(ab) = e^(cd) * e^(pq)