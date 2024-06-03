from fractions import Fraction

# system of equations
# 2x + 8y = 79445x + 3y

# simplified
# 79443x -5y = 0

# phi
# phi(x) = g^x mod p

# phi-ify our system
# g^(79443x-5y) mod p = 0

# to work with whole numbers, rely on g^(a/b) mod p = (g^a * g^-b) mod p

g = 2
p = 4783

def validateSolution(solutionX, solutionY):
    ## equation 1 zk-proof (validates equation 1)
    power = 2 * solutionX + 8 * solutionY
    intermediary = pow(g, power.numerator.numerator, p) * pow(power.denominator.numerator, -1, p)
    result = pow(intermediary, 1, p)
    knowsSolution = result == pow(g, 4764, p)
    print(f'equation 1 validated: {knowsSolution}')

    ## equation 2 zk-proof (validates equation 2)
    power = 79445 * solutionX + 3 * solutionY
    intermediary = pow(g, power.numerator.numerator, p) * pow(power.denominator.numerator, -1, p)
    result = pow(intermediary, 1, p)
    knowsSolution = result == pow(g, 4764, p)
    print(f'equation 2 validated: {knowsSolution}')

    ## composite equation zk-proof (validates the whole system)
    power = 79443 * solutionX + -5 * solutionY
    intermediary = pow(g, power.numerator.numerator, p) * pow(power.denominator.numerator, -1, p)
    result = pow(intermediary, 1, p)
    knowsSolution = result == 1
    print(f'equation 3 validated: {knowsSolution}')

    ## euler's totient zk-proof (validates the whole system)
    ## g^(79443x-5y) mod p = g^0 mod p can be simplified via Euler's totient to
    ## 79443x - 8y mod (p - 1) = 0
    power = 79443 * solutionX - 5 * solutionY
    a = power.numerator.numerator
    b = power.denominator.numerator
    intermediary = a * pow(b, -1)
    result = pow(int(intermediary), 1, p - 1)
    knowsSolution = result == 0
    print(f'equation 4 validated: {knowsSolution}')


# solution for this system of equations (validate on wolfram alpha)
solutionX = Fraction(numerator=11910, denominator=317777)
solutionY = Fraction(numerator=189233226, denominator=317777)
print('validate correct solution')
validateSolution(solutionX, solutionY)
print('\n\n')

solutionX = Fraction(numerator=11911, denominator=317777)
solutionY = Fraction(numerator=189233221, denominator=317777)
print('incorrect solution')
validateSolution(solutionX, solutionY)
print('\n\n')
