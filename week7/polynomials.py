from numpy import poly1d

p1 = poly1d([10, 9, 4, -6])
p2 = poly1d([4, 2])
print(p1)
print(p2)
print(p1 * p2)

x = 5
y = 5
outcome = 3*y*(x**2) + 5*x*y - x - 2*x*y + 3
print(f'outcome: {outcome}')