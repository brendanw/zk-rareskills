from fractions import Fraction

x = Fraction(53, 192)
y = Fraction(61, 511)
# some fraction a / b
sum = x + y
print(f'sum: {sum}')
# (a / b) mod 1033 = (a * b^-1) mod 1033
a = sum.numerator.numerator
b = sum.denominator.numerator
toModSpace = pow((pow(a, 1, 1033) * pow(b, -1, 1033)), 1, 1033)
print(f'toModSpace = {toModSpace}')

# expanded form
left = pow((pow(53, 1, 1033) * pow(192, -1, 1033)), 1, 1033)
right = pow((pow(61, 1, 1033)*pow(511, -1, 1033)), 1, 1033)
modSum = pow((left + right), 1, 1033)

print(f'expanded modspace sum: {modSum}')