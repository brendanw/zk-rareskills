from py_ecc.bn128 import G1, multiply, add

# Prover
secret_x = 7

# input to verifier
A = multiply(G1, secret_x)

proof = (A, 15)
print(f'proof: {proof}')

lefthand = multiply(G1, 161)
righthand = multiply(A, 23)
print(f'lefthand: {lefthand}')
print(f'righthand: {righthand}')


# verifier
if lefthand == righthand:
    print("statement is true")
else:
    print("statement is false")