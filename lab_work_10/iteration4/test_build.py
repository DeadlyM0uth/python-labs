import iteration4

print('sin integral approx:', iteration4.integrate_cython(iteration4.my_sin, 0.0, 3.141592653589793, 10000))
print('square integral approx:', iteration4.integrate_cython(iteration4.square, 0.0, 1.0, 10000))
