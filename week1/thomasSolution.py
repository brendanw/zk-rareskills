def make_proof(x, y, g, n):
    """
    Compute phi(x), phi(y)
    This is a one way function and verifier will not be able to reverse it
    """
    x_ = pow(g, x, n)
    y_ = pow(g, y, n)
    return x_, y_

def validate(phix, phiy, g, n):
    """
    # Convert all the multiplications to addition, so we're doing:
    # x + x + y + y + y.... etc
    """
    valid1 = phix*phix * phiy*phiy*phiy*phiy*phiy*phiy*phiy*phiy == pow(g, 7944, n)
    valid2 = phix*phix*phix*phix*phix * phiy*phiy*phiy == pow(g, 4764, n)
    return valid1 and valid2

x=420
y=888
g = 7
n = 13
phix, phiy = make_proof(x, y, g, n)
valid = validate(phix, phiy, g, n)
print(valid)

for i in range(20_000):
    for j in range(20_000):
        phix, phiy = make_proof(i, j, g, n)
        valid = validate(phix, phiy, g, n)
        if valid:
            print(f'found solution: {i}, {j}')