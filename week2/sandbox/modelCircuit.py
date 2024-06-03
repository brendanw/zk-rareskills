import galois

GF103 = galois.GF(103)

# we define a polynomial x^2 + 2x + 102 mod 103
p1 = galois.Poly([1, 2, 102], GF103)

print(p1)

p2 = galois.Poly([1, 1, 1], GF103)

print(p2)

print(p1 + p2)

print("------")

p3 = galois.Poly([-1, 1], GF103)
p4 = galois.Poly([-1, 2], GF103)

print(p3)
print(p4)
print(p3*p4)
print((p3*p4).roots())