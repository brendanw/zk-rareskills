from py_ecc.bn128 import neg, add, multiply, G1, G2, pairing, G12, is_inf, eq

# greek letters confuse me, so I've replaced them with normal letters such that we are validating
# 0 = e(-A1, B2) + e(D1, H2) + e(X1, Y2) + e(C1, J2)
#
# where X1 = x1 + x2 + x3
#
# AND
#
# A1 = a * G1
# B2 = b * G2
# D1 = d * G1
# H2 = h * G2
# X1 = (x1 + x2 + x3) * G1
# Y2 = y * G2
# C1 = c * G1
# J2 = j * J2
#
# alternatively we can thus write
#
# 0 = -a * b + d * h + (x1 + x2 + x3) * y + c * j OR ab = dh + (x1 + x2 + x3) * y + c * j
#
# caller passes in A1, B2, C1, and thus defines a, b, c, x1, x2, x3
# thus we must pre - define / hardcode d, h, y, and j
#
# this function assumes
# d = 5 D1 = 5 * G1
# h = 12 H2 = 12 * G2
# y = 3 Y2 = 3 * G2
# j = 2 J2 = 2 * G2
#
# thus a valid solution is:
# x1 = 1, x2 = 2, x3 = 3 where X1 = 6
# a = 2 A1 = 2 * G1
# b = 42 B2 = 42 * G2
# c = 3 C1 = 3 * G1

D1 = multiply(G1, 5)
H2 = multiply(G2, 12)
Y2 = multiply(G2, 3)
J2 = multiply(G2, 2)


def verify(x1: int, x2: int, x3: int, A1, B2, C1):
    X1 = multiply(G1, x1 + x2 + x3)

    AB = pairing(B2, neg(A1))
    DH = pairing(H2, D1)
    XY = pairing(Y2, X1)
    CJ = pairing(J2, C1)
    result = AB * DH * XY * CJ
    return result

# correct solution
a = 2
b = 42
c = 3
solA1 = multiply(G1, a)
solB2 = multiply(G2, b)
solC1 = multiply(G1, c)
result = verify(1, 2, 3, solA1, solB2, solC1)
print(f'result: {result}')
