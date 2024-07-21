from numpy import poly1d
print(f'{poly1d([1, -10])}')
# (x - 10) * (2x + 5)
h = poly1d([1, -10])*poly1d([2, 5])
# (x - 1) * (x - 2) * (x - 3)
t = poly1d([1, -1])*poly1d([1, -2])*poly1d([1, -3])

tau = 14
# our algorithm evaluates using the method of the last element, but in encrypted form
assert (h*t)(tau) == h(tau)*t(tau) == poly1d(t(tau) * h)(tau), "tau evaluations don't match"

print('done')