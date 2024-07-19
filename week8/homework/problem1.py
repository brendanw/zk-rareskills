from functools import reduce

import numpy as np
import random
from scipy.interpolate import lagrange
from numpy.typing import NDArray
from numpy import poly1d
import galois
from py_ecc.bn128 import G1, G2, add, curve_order, multiply, neg, Z1, pairing

# See homework8.png to see homework problem
# An R1CS is represented by Ls * Rs = Os where s is a solution/witness vector and * represents hammard product
# A QAP is a polynomial representation of this equivalency that evaluates to true at n given points

# let's start with an arbitrary R1CS to convert to a QAP
# we'll reuse the R1CS from last week's homework. we already know the solution is x=100, y=100
# last week's homework was an RCS representation of out = 3yx^2 + 5xy - x - 2xy + 3
# the below will copy and paste setup from week7 homework so we can get U, V, W, HT

# this really ought to match the curve order TODO: update this to use curve_order later
fieldOrder = 79
GF = galois.GF(fieldOrder)

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

U = inner_product_polynomials_with_witness(U_polys, w)
V = inner_product_polynomials_with_witness(V_polys, w)
W = inner_product_polynomials_with_witness(W_polys, w)

# t = (x - 1)(x - 2)(x - 3)(x - 4)
t = galois.Poly([1, 78], field = GF) * galois.Poly([1, 77], field = GF) * galois.Poly([1, 76], field = GF)

# t is gonna be of degree 3 which still doesn't match the lefthand side which will be of degree 4
# so we use some algebra and the nifty factoid that
# When two non-zero polynomials are multiplied, the roots of the product is the union of the roots of the individual polynomials

h = (U * V - W) // t

# remember that only the prover can produce U,V,W,and h. The verifier also knows t(x)
print(f'U = {U}')
print(f'V = {V}')
print(f'W = {W}')
print(f'h = {h}')
print(f't = {t}')

# let's do the trusted setup

# we compute tau as some random number (should pick something larger, but this will do for now)
tau = GF(8)

def generate_powers_of_tau_G1(tau, degree):
    return [multiply(G1, int(tau ** i)) for i in range(degree + 1)]

def generate_powers_of_tau_G2(tau, degree):
    return [multiply(G2, int(tau ** i)) for i in range(degree + 1)]

# we compute G1 SRS
g1_srs = generate_powers_of_tau_G1(tau, 3)

# we compute G2 SRS
g2_srs = generate_powers_of_tau_G2(tau, 3)

# we compute T(tau) SRS. TODO: I was confused about what we are actually computing for the SRS. Does the SRS become an array of polynomials?
t_srs = []

def inner_product(ec_points, coeffs):
    return reduce(add, (multiply(point, int(coeff)) for point, coeff in zip(ec_points, coeffs)), Z1)

# Now we compute [A]1, [B]2, [C']1, [HT]1

# evaluate U polynomial with G1 SRS to produce [A]1
A = inner_product(g1_srs, U.coeffs[::-1])
print(f'A = {A}')

# evaluate V polynomial with G2 SRS to produce [B]2
B = inner_product(g2_srs, V.coeffs[::-1])
print(f'B = {B}')

# evaluate W polynomial with G1 SRS to produce [C']1
Cprime = inner_product(g1_srs, W.coeffs[::-1])
print(f'Cprime = {Cprime}')

# evaluate HT polynomial with T(tau) SRS to produce [HT]1
ht = h * t
HT = inner_product(g1_srs, ht.coeffs[::-1])
print(f'HT = {HT}')
# TODO: there is another way to compute HT where verifier supplies T, I need to figure out how to do that

# evaluate [C] = [C']1 + [HT]1
C = add(Cprime, HT)
print(f'C = {C}')

# verifier validates e([A]1,[B]2) - e([C]1,[G]2) = 0
left = pairing(B,A)
right = pairing(G2, C)
print(f'left = {left}')
print(f'right = {right}')
zeroG12 = left - right
# below should be G12
print(f'zeroG12 = {zeroG12}')

# TODO: bonus points to have verifier validate that (a) G1 and G2 points match for trusted setup. (b) each subsequent set
# of G1 and G2 points is the square of the previous points