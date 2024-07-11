import numpy as np
from numpy.typing import NDArray
from typing import Any
from py_ecc.bn128 import G1, G2, add, curve_order, multiply, neg, pairing, eq

# Given an R1CS of the form
# L\mathbf{\vec{[s]_1}}\odot R\mathbf{\vec{[s]_2}} = O\mathbf{\vec{[s]}_{1}}\odot\vec{[G_2]_2}
# Where L, R, and O are n x m matrices of field elements and s is a vector of G1, G2, or G1 points
# Write python code that verifies the formula.

# You can check the equality of G12 points in Python this way:
# a = pairing(multiply(G2, 5), multiply(G1, 8))
# b = pairing(multiply(G2, 10), multiply(G1, 4))
# eq(a, b)

# Hint: Each row of the matrices is a separate pairing.
# When you get s encrypted with both G1 and G2 generators, you don’t know whether or not they have the same discrete
# logarithm. However, it is straightforward to check using another equation. Figure out how to discover if sG1 == sG2
# if you are given the elliptic curve points but not s.

# for simplicity we'll assume we are modeling
# xy = v
# v*v = w
#
# 2 * 3 = 6
# 6 * 6 = 36
#

L = np.array([
    [0,1,0,0,0],
    [0,0,0,1,0]
])

R = np.array([
    [0,0,1,0,0],
    [0,0,0,1,0]
])

O = np.array([
    [0,0,0,1,0],
    [0,0,0,0,1]
])

def verifyEquation(s1: NDArray[Any], s2: NDArray[Any]) -> bool:
    assert len(s1) == len(s2)
    # validate that all s1 and s2 points are equivalent points in G1<->G2 space
    for j in range(len(s1)):
        left = pairing(multiply(G2, 5), s1[j])
        right = pairing(s2[j], multiply(G1, 5))
        assert(eq(left, right))

    A = np.dot(L,s1)
    B = np.dot(R,s2)
    C = np.dot(O,s1)
    for i in range(len(L)):
        left = pairing(B[i], A[i])
        right = pairing(G2, C[i])
        if not eq(left, right):
            return False
    return True

s1 = np.array([G1, multiply(G1,2),multiply(G1, 3),multiply(G1, 6),multiply(G1, 36)])
s2 = np.array([G2, multiply(G2, 2),multiply(G2, 3),multiply(G2, 6),multiply(G2, 36)])
assert(verifyEquation(s1, s2) == True)

s1 = np.array([G1, multiply(G1, 2), multiply(G1, 3), multiply(G1, 6), multiply(G1, 35)])
s2 = np.array([G2, multiply(G2, 2), multiply(G2, 3), multiply(G2, 6), multiply(G2, 35)])
assert(verifyEquation(s1, s2) == False)

# we expect an assertion error below
s1 = np.array([G1, multiply(G1, 3), multiply(G1, 3), multiply(G1, 6), multiply(G1, 35)])
s2 = np.array([G2, multiply(G2, 2), multiply(G2, 3), multiply(G2, 6), multiply(G2, 35)])
assert(verifyEquation(s1, s2) == False)

print('finished')