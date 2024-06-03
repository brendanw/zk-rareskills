a = 5
n = 100
a_inv = a ** (n - 2) % n
print(f"a_inv={a_inv}")
print(a_inv * a % n == 1)

