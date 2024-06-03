from libnum import has_sqrtmod_prime_power, sqrtmod_prime_power

# tells us if (5 mod 11) has a square root
print(has_sqrtmod_prime_power(5, 11, 1))

# gives the square roots of (5 mod 11)
print(list(sqrtmod_prime_power(5, 11, 1)))

# this function works for p = 4k + 3
def mod_sqrt(x, p):
    assert (p - 3) % 4 == 0, "prime not 4k + 3"
    exponent = (p + 1) // 4
    return pow(x, exponent, p)  # x ^ e % p

print(mod_sqrt(5, 23))