import numpy as np

A = np.array([[2, 8], [79445, 3]])
b = np.array([4764, 4763])

solution = np.linalg.solve(A, b)

print(np.array2string(solution, formatter={'float_kind': lambda x: "%.2f" % x}))

x, y = solution

# non-zk proof
system1 = 2*x + 8*y
system2 = 79445*x + 3*y
print(f'system1: {system1}')
print(f'system2: {system2}')

# zk proof in non-code
# where phi(x) = 2^x mod 7
# (phi(x))^2 + (phi(y))^8 = (phi(x))^79445 + (phi(y))^3

# zero-knowledge proof without modulus

lefthand = pow(2, 2 * x) + pow(2, 8 * y)
righthand = pow(2, 79445 * x) + pow(2, 3 * y)

print(f'lefthand: {lefthand}')
print(f'righthand: {righthand}')

# zk proof w/ modulus

left = pow(2, 2 * x, 7) + pow(2, 8 * y, 7)

print(f'left: {left}')



