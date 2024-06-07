from py_ecc.bn128 import G1, multiply, add

# Prover
secret_x = 2

# input to verifier
A = multiply(G1, secret_x)

proof = (A, 14)
print(f'proof: {proof}')

lefthand = multiply(G1, 14)
righthand = multiply(A, 7)
print(f'lefthand: {lefthand}')
print(f'righthand: {righthand}')


# verifier
if lefthand == righthand:
    print("statement is true")
else:
    print("statement is false")