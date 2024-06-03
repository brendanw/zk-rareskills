import myfrac

def mod_inverse(a, m):
    # Function to return the multiplicative inverse of a under modulo m
    m0, y, x = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        y = x - q * y
        x = t
    if x < 0:
        x = x + m0
    return x

# Constants
g = 2
p = 4783

# Accurate values converted to fractions
fractionX = fractions.Fraction(numerator=3970, denominator=105939)
fractionY = fractions.Fraction(numerator=63085682, denominator=105939)

# Calculate modular inverses
inv_denominatorX = mod_inverse(fractionX.denominator, p - 1)
inv_denominatorY = mod_inverse(fractionY.denominator, p - 1)

# Calculate accurate values in the modular field
mod_accurateX = (fractionX.numerator * inv_denominatorX) % (p - 1)
mod_accurateY = (fractionY.numerator * inv_denominatorY) % (p - 1)

# Perform calculations in the modular field
shouldZero = (79443 * mod_accurateX - 5 * mod_accurateY) % (p - 1)
eq1 = (2 * mod_accurateX + 8 * mod_accurateY) % (p - 1)
eq2 = (79445 * mod_accurateX + 3 * mod_accurateY) % (p - 1)

print(f'shouldZero: {shouldZero}')
print(f'2x + 8y = {eq1} == 4764 mod (p-1)')
print(f'79445x + 3y = {eq2} == 4764 mod (p-1)')