from py_ecc.bn128 import G1, add, curve_order, multiply, neg

print(neg(G1))
print(multiply(G1, curve_order))
print(multiply(G1, curve_order - 1))