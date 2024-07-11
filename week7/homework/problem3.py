from functools import reduce

import numpy as np
import random
from scipy.interpolate import lagrange
from numpy.typing import NDArray
from numpy import poly1d
import galois

# Refer to the code here: https://www.rareskills.io/post/r1cs-to-qap
#
# Do the same operation R1CS above but convert it to a QAP over a finite field. Don’t do it by hand, use Python. If you
# pick GF79 like the article does, you’ll need to find the congruent element in the field since some of the scalar
# values for the R1CS above will be negative or be larger than 79.

# this really ought to match the curve order
GF = galois.GF(79)

L = np.array([[0,0,3,0,0,0],
               [0,0,0,0,1,0],
               [0,0,1,0,0,0]])

R = np.array([[0,0,1,0,0,0],
               [0,0,0,1,0,0],
               [0,0,0,5,0,0]])

O = np.array([[0,0,0,0,1,0],
               [0,0,0,0,0,1],
               [76,1,1,2,0,78]])

L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

x = GF(21)
y = GF(21)

out = 3 * x * x * y + 5 * x * y + GF(78)*x + GF(79 - 2) * y + GF(3)
v1 = 3*x*x
v2 = v1 * y
w = GF(np.array([1, out, x, y, v1, v2]))

assert all(np.equal(np.matmul(L_galois, w) * np.matmul(R_galois, w), np.matmul(O_galois, w))), "not equal"

def interpolate_column(col):
    xs = GF(np.array([1,2,3]))
    return galois.lagrange_poly(xs, col)

U_polys = np.apply_along_axis(interpolate_column, 0, L_galois)
V_polys = np.apply_along_axis(interpolate_column, 0, R_galois)
W_polys = np.apply_along_axis(interpolate_column, 0, O_galois)

def inner_product_polynomials_with_witness(polys, witness):
    mul_ = lambda x, y: x * y
    sum_ = lambda x, y: x + y
    return reduce(sum_, map(mul_, polys, witness))

term_1 = inner_product_polynomials_with_witness(U_polys, w)
term_2 = inner_product_polynomials_with_witness(V_polys, w)
term_3 = inner_product_polynomials_with_witness(W_polys, w)

# t = (x - 1)(x - 2)(x - 3)(x - 4)
t = galois.Poly([1, 78], field = GF) * galois.Poly([1, 77], field = GF) * galois.Poly([1, 76], field = GF)

h = (term_1 * term_2 - term_3) // t

left = term_1 * term_2
right = term_3 + h * t
print(left)
print(right)

assert term_1 * term_2 == term_3 + h * t, "division has a remainder"