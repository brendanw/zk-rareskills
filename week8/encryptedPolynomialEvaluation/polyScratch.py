from py_ecc.bn128 import G1, multiply, add, curve_order, eq, Z1
from functools import reduce
import galois

GF = galois.GF(113)
p = galois.Poly([1, -4], field=GF) * galois.Poly([1, 2], field=GF)
print(f'p: {p}')

print(f'p.coeffs: {p.coeffs}')
myCoefficients = p.coeffs[::-1]
print(f'myCoefficients: {myCoefficients}')