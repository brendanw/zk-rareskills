# equation 1: 2x + 8y = 7944
# equation 2: 5x + 3y = 4764

g = 2 # g must be a prime number
p = 7951 # p must be a prime number larger than 7944 to prevent false positive

def phi(x):
    return pow(g, x, p)

# prove solution works for equation 1 (2x + 8y = 7944)
def firstProof(x, y):
    lefthand = pow(pow(g, (2 * x) + (8 * y), p), 1, p)
    righthand = pow(g, 7944, p)
    # print(f'x={x} y={y} satisfies 2x+8y=7944: {lefthand == righthand}')
    return lefthand == righthand

# prove solution works for equation 2 (5x + 3y = 4764)
def secondProof(x, y):
    lefthand = pow(pow(g, 5 * x + 3 * y, p), 1, p)
    righthand = phi(4764)
    # print(f'x={x} y={y} satisfies 2x+8y=4764: {lefthand == righthand}')
    return lefthand == righthand

def proveSumComputationWasPerformed(x, y):
    return firstProof(x, y) and secondProof(x, y)

def checkSol(x, y):
    firstProof(x, y)
    secondProof(x, y)
    # combined systems proof
    # print(f'does sol work for both solutions: {combined(x, y)}\n\n')

checkSol(420, 888)
checkSol(420, 887)
checkSol(0, 0)
checkSol(1, 1)

for i in range(20_000):
    for j in range(20_000):
        valid = proveSumComputationWasPerformed(i, j)
        if valid:
            print(f'found solution: {i} and {j}')
