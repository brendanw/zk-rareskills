import galois

# finite fields are sometimes called Galois Fields

GF11 = galois.GF(11)

three_two = GF11(1) / GF11(8)
print(three_two)

one_half = GF11(1) / GF11(2)
print(one_half)
