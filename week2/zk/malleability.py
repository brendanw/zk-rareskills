from py_ecc.bn128 import G1, multiply, add, neg

order = 21888242871839275222246405745257275088548364400416034343698204186575808495617
x = 100 # chosen randomly
assertion = multiply(G1, order - x) == neg(multiply(G1, x))
print(assertion)

