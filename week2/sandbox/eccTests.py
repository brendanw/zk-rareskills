from py_ecc.bn128 import curve_order, add, field_modulus, G1, multiply, eq

print(f'field_modulus: {field_modulus}')
print(f'curve_order: {curve_order}')
print(f'diff: {field_modulus - curve_order}')

x = 5 # chosen randomly
# This passes
print(eq(multiply(G1, x), multiply(G1, x + curve_order)))

# This fails
print(eq(multiply(G1, x), multiply(G1, x + field_modulus)))

print('---------')

# 2^(300 + 21)
x = 2 ** 300 + 21
# 2^(50 + 11)
y = 3 ** 50 + 11

# (x + y) == xG + yG
result = eq(multiply(G1, (x + y)), add(multiply(G1, x), multiply(G1, y)))
print(result)

# G1 * ((x + y) mod curve_order) === G1 * x + G1 * y
result2 = eq(multiply(G1, (x + y) % curve_order), add(multiply(G1, x), multiply(G1, y)))
print(result2)

# G1 * ((x+y) mod (curve_order-1)) === G1 * x + G1 * y
thisBreaks = eq(multiply(G1, (x + y) % (curve_order - 1)), add(multiply(G1, x), multiply(G1, y)))
print(thisBreaks)

print('------------')
five_over_two = (5 * pow(2, -1, curve_order)) % curve_order
one_half = pow(2, -1, curve_order)

# (5g/2 + g/2) === 3g
result = eq(add(multiply(G1, five_over_two), multiply(G1, one_half)), multiply(G1, 3))
print(result)
print('---------------')

# associativity
# (xg + yg) + zg === xg + yg + zg
x = 5111111111111
y = 1000001111111
z = 1511111111

lhs = add(add(multiply(G1, x), multiply(G1, y)), multiply(G1, z))
rhs = add(multiply(G1, x), add(multiply(G1, y), multiply(G1, z)))
result = eq(lhs, rhs)
print(result)

