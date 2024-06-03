g = 2
p = 4783

accurateX = 0.0375
accurateY = 595.490625

# this
exp = (79443 * accurateX) - (5 * accurateY)
print(f'exp: {exp}')

#
left = g ** round(exp, 2) % p
right = pow(g, 4764, p)
print(f'left: {left}')
print(f'right: {right}')