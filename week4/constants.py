from py_ecc.bn128 import neg, add, multiply, G1, G2, pairing, G12, is_inf, eq

D1 = multiply(G1, 5)
H2 = multiply(G2, 12)
Y2 = multiply(G2, 3)
J2 = multiply(G2, 2)

print(f'D1: {D1}')
print(f'H2: {H2}')
print(f'Y2: {Y2}')
print(f'J2: {J2}')

a = 2
b = 42
c = 3
solA1 = multiply(G1, a)
solB2 = multiply(G2, b)
solC1 = multiply(G1, c)

print(f'solA1: {solA1}')
print(f'solB2: {solB2}')
print(f'solC1: {solC1}')
