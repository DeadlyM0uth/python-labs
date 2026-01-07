import iteration4 as cy
import math


n_iter = 1_000_000

print(cy.integrate_cython(cy.my_sin, 0, math.pi, n_iter))

