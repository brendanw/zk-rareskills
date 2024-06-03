from py_ecc.bn128 import G1, multiply, neg, add, is_inf, Z1, eq

# pick a field element
x = 12345678 # generate the point
p = multiply(G1, x)

# invert
p_inv = neg(p)

print(f'Px={p[0]} Py={p[1]}')
print(f'PInvX={p_inv[0]} PInvY={p_inv[1]}')

print(f'{add(p_inv, p)}')

# every element added to its inverse produces the identity element
# assert is_inf(add(p, p_inv))

# Z1 is just None, which is the point at infinity
print(f'z1 is none: {Z1 is None}')

# special case: the inverse of the identity is itself
result = eq(neg(Z1), Z1)
print(result)

print('-----------------\n\n')

field_modulus = 21888242871839275222246405745257275088696311157297823662689037894645226208583
for i in range(1, 4):
    print('----')
    point = multiply(G1, i)
    print(point)
    print(neg(point))

    # x values are the same
    assert int(point[0]) == int(neg(point)[0])

    # y values are inverses of each other, we are adding y values
    # not ec points
    assert int(point[1]) + int(neg(point)[1]) == field_modulus

    sum = int(point[1]) + int(neg(point)[1])
    print((sum % field_modulus) == 0)