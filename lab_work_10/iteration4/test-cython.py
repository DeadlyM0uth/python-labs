import integrate_cython as cy
import math


n_iter = 10_000_000

print(cy.integrate_cython(math.sin, 0, math.pi, n_iter))

