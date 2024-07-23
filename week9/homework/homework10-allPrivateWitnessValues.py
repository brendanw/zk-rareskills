from functools import reduce

import numpy as np
import random
from scipy.interpolate import lagrange
from numpy.typing import NDArray
from numpy import poly1d
import galois
from py_ecc.bn128 import G1, G2, add, curve_order, multiply, neg, Z1, Z2, pairing
from sympy import summation

# ret2basic has decent implementation of groth16 at https://github.com/ret2basic/Groth16/blob/main/groth16.py

# QAP. We will take QAP from last week's homework that represents out = 3yx^2 + 5xy - x - 2xy + 3
# for the first rendition we will make all values of the witness private for simplicity
fieldOrder = curve_order # 557 is a small prime number
GF = galois.GF(fieldOrder)

L = np.array([[0,0,3,0,0,0],
               [0,0,0,0,1,0],
               [0,0,1,0,0,0]])

R = np.array([[0,0,1,0,0,0],
               [0,0,0,1,0,0],
               [0,0,0,5,0,0]])

O = np.array([[0,0,0,0,1,0],
               [0,0,0,0,0,1],
               [(fieldOrder - 3),1,1,2,0,(fieldOrder - 1)]])

L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

x = GF(21)
y = GF(21)

out = 3 * x * x * y + 5 * x * y + GF(fieldOrder - 1)*x + GF(fieldOrder - 2) * y + GF(3)
v1 = 3*x*x
v2 = v1 * y
witness = GF(np.array([1, out, x, y, v1, v2]))

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

U = inner_product_polynomials_with_witness(U_polys, witness)
V = inner_product_polynomials_with_witness(V_polys, witness)
W = inner_product_polynomials_with_witness(W_polys, witness)

# t = (x - 1)(x - 2)(x - 3)
t = galois.Poly([1, (fieldOrder - 1)], field = GF) * galois.Poly([1, (fieldOrder - 2)], field = GF) * galois.Poly([1, (fieldOrder - 3)], field = GF)

# t is gonna be of degree 3 which still doesn't match the lefthand side which will be of degree 4
# so we use some algebra and the nifty factoid that
# When two non-zero polynomials are multiplied, the roots of the product is the union of the roots of the individual polynomials
h = (U * V - W) // t

ht = h * t

# Trusted setup
tau = GF(8)

def generate_powers_of_tau_G1(tau, degree):
    return [multiply(G1, int(tau ** i)) for i in range(degree + 1)]

def generate_powers_of_tau_G2(tau, degree):
    return [multiply(G2, int(tau ** i)) for i in range(degree + 1)]

# we compute G1 SRS
g1_srs = generate_powers_of_tau_G1(tau, 4)

# we compute G2 SRS
g2_srs = generate_powers_of_tau_G2(tau, 4)

# we compute T(tau) SRS for h(tau)t(tau)
t_srs = []
for i in range(len(g1_srs)):
    tauRaisedToI = tau ** i
    tAtTau = GF(t(tau))
    coefficient = tauRaisedToI * tAtTau
    element = multiply(G1, int(coefficient))
    t_srs.append(element)

# we compute alpha shift
alpha = GF(113)
alphaG = multiply(G1, int(alpha))

# we compute beta shift
beta = GF(211)
betaG = multiply(G2, int(beta))

# we compute powers of tau for C. U_polys will be of length 6 since that is the witness size
# I validated that my code outputs the exact same as ret2basic's omega generation code if I
# copy and paste his in here
omega_srs = []
for i in range(len(U_polys)):
    wPoly = W_polys[i]
    uPoly = beta * U_polys[i]
    vPoly = alpha * V_polys[i]
    finalPoly = wPoly + uPoly + vPoly
    summation = finalPoly(tau)
    encrypted = multiply(G1, int(summation))
    omega_srs.append(encrypted)

def inner_product(ec_points, coeffs):
    return reduce(add, (multiply(point, int(coeff)) for point, coeff in zip(ec_points, coeffs)), Z1)

# Prover computes witness vector
# I sanity checked summationOfUAtTau matches my value from last week's homework
summationOfUAtTau = inner_product(g1_srs, U.coeffs[::-1])

A = add(alphaG, summationOfUAtTau)
print(f'A: {A}')

# I sanity checked summationOfVAtTau matches my value from last week's homework
summationOfVAtTau = inner_product(g2_srs, V.coeffs[::-1])

B = add(betaG, summationOfVAtTau)
print(f'B: {B}')

# Z1 is point at infinity
omegaSummation = Z1
for i in range(len(omega_srs)):
    elem = multiply(omega_srs[i], int(witness[i]))
    omegaSummation = add(omegaSummation, elem)

powers_of_tau_for_inputs = [multiply(entry, int(witness[i])) for entry in omega_srs]
altOmegaSummation = inner_product(omega_srs, witness)
print(f'omegaSummation: {omegaSummation}')
print(f'altOmegaSummation: {altOmegaSummation}')
# summation and altSummation are the same, I checked!

HT = inner_product(t_srs, h.coeffs[::-1])
print(f'HT: {HT}')

C = add(altOmegaSummation, HT)
print(f'C: {C}')

# Verifier validates that `e(G2, C) + e(alphaG, betaG) - e(B2,A1) === 0`
alphaBeta = pairing(betaG, alphaG)
AB = pairing(B,A)
C12 = pairing(G2, C)
I12 = alphaBeta + C12 - AB
print(f'I12 = {I12}')

newOutcome = pairing(betaG, alphaG) + pairing(G2, C) - pairing(B, A)
print(f'newOutcome = {newOutcome}')

# verify simple version without alpha and beta
CPrime = inner_product(g1_srs, W.coeffs[::-1])
oldC = add(CPrime, HT)
oldOutcome = pairing(summationOfVAtTau, summationOfUAtTau) - pairing(G2, oldC)
print(f'oldOutcome = {oldOutcome}')