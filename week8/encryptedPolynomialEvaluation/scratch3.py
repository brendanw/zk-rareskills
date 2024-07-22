from functools import reduce

import numpy as np
import random
from scipy.interpolate import lagrange
from numpy.typing import NDArray
from numpy import poly1d
import galois
from py_ecc.bn128 import G1, G2, add, curve_order, multiply, neg, Z1, Z2, pairing, G12

# 341x^2 + 237x + 296

def inner_product(ec_points, coeffs):
    return reduce(add, (multiply(point, int(coeff)) for point, coeff in zip(ec_points, coeffs)), Z1)

def generate_powers_of_tau(tau, degree):
    return [multiply(G1, int(tau ** i)) for i in range(degree + 1)]

GF = galois.GF(curve_order)

tau = GF(8)

u = galois.Poly([341, 237, 296], field = GF)
print(f'u: {u}')

# we compute G1 SRS
powers_of_tau = generate_powers_of_tau(tau, u.degree)
print(f'powers_of_tau = {powers_of_tau}')

A = inner_product(powers_of_tau, u.coeffs[::-1])
altA = multiply(G1, int(u(tau)))

print(f'A: {A}')
print(f'altA: {altA}')

assert A == altA, "wtf?"