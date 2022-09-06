from dis import dis
from math import sqrt
import sys

a = float(sys.argv[1])
b = float(sys.argv[2])
c = float(sys.argv[3])

print(f'y = {a}x^2 + ({b})x^2 + ({c})')
print()

discrim = b**2 - 4*a*c

print(f'discrim = {b}^2 - 4({a})({c}) = {discrim}')

if discrim < 0:
    print('    has no real roots (discrim < 0)')
    exit(0)
elif discrim > 0:
    print('    has two solutions (discrim > 0)')
else:
    print('    has repeated root (discrim = 0)')

print()

root1 = round((-b + sqrt(discrim)) / (2*a), 3)
root2 = round((-b - sqrt(discrim)) / (2*a), 3)

print(f'x = (-{b} +- sqrt({discrim})) / (2({a}))')

if root1 == root2:
    print(f'x = {root1}')
else:
    print(f'x = {root1}, x = {root2}')

h = round((root1 + root2) / 2, 3)
k = round(a*h**2 + b*h + c, 3)

print()
print(f'h = ({root1} + {root2})/2 = {h}')
print(f'k = {a}({h})^2 + ({b})({h}) + ({c}) = {k}')
print(f'y = {a}(x - ({h}))^2 + ({k})')