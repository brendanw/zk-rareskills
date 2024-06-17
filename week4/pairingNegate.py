from py_ecc.bn128 import neg, add, multiply, G1, G2, pairing, G12, is_inf, eq

pairing(G2, G1)
pairing(neg(G2), neg(G1))