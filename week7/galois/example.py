import numpy as np
import galois

# we want to encode: out = x^4 - 5*y^2*x^2

x = 4
y = -2

v1 = x * x # x^2
v2 = v1*v1 # x^4
v3 = -5*y * y
out = v3*v1 + v2

witness = np.array([1, out, x, y, v1, v2, v3])

# we will use the prime number 79
# Lw * Rw = Ow

L = np.array([
    #1, o, x, y,v1,v2,v3
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, -5, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
])

R = np.array([
    #1, o, x, y,v1,v2,v3
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
])

# v3*v1 = out - v2
O = np.array([
    #1, o, x, y,v1,v2,v3
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, -1, 0],
])

assert all(np.equal(np.matmul(L, witness) * np.matmul(R, witness), np.matmul(O, witness))), "not equal"

GF = galois.GF(79)
a = GF(70)
b = GF(10)
print(a + b)

L = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 74, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1],
])

R = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
])

O = np.array([
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 78, 0],
])

L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

x = GF(4)
y = GF(79-2)

v1 = x * x # x^2
v2 = v1*v1 # x^4
v3 = GF(79-5)*y * y
out = v3*v1 + v2

witness = GF(np.array([1, out, x, y, v1, v2, v3]))

assert all(np.equal(np.matmul(L_galois, witness) * np.matmul(R_galois, witness), np.matmul(O_galois, witness))), "not equal"

def interpolate_column(col):
    xs = GF(np.array([1,2,3,4]))
    return galois.lagrange_poly(xs, col)

U_polys = np.apply_along_axis(interpolate_column, 0, L_galois)
print(U_polys)