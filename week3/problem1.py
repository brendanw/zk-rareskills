from py_ecc.bn128 import G1, add, curve_order, multiply, neg

# (3/5) + (4/5) = (7/5)
# (3/5)G + (4/5)G = (7/5)G

A = multiply(G1, 3 * pow(5, -1, curve_order))
B = multiply(G1, 4 * pow(5, -1, curve_order))
print(f'A: {A}')
print(f'B: {B}')

C = multiply(G1, 7 * pow(5, -1, curve_order))

lefthand = add(A, B)
print(lefthand == C)

print(curve_order)

print(G1)
