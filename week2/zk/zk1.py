from py_ecc.bn128 import G1, multiply, add, curve_order

# Prover
secret_x = 5
secret_y = 10

x = multiply(G1, 5)
y = multiply(G1, 10)

proof = (x, y, 15)
print(f'proof: {proof}')

# verifier
if multiply(G1, proof[2]) == add(proof[0], proof[1]):
    print("statement is true")
else:
    print("statement is false")