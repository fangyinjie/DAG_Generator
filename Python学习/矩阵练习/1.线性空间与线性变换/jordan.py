import numpy as np
from sympy import Matrix
import sympy
import pprint

#A = np.array([[3,1,0,0],[-4,-1,0,0],[6,2,0,-1],[-2,0,1,2]])
A = np.array([
    [4,9,2],
    [3,5,7],
    [8,1,6]])
"""
A = np.array([[0, 1, 0, 0, 1, 1, 0],
              [0, 0, 1, 0, 1, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 1, 0, 1, 1],
              [0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0]])
"""
a = Matrix(A)
P, Ja = a.jordan_form()

pprint.pprint(Ja)
pprint.pprint(P)