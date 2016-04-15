from pymongo import MongoClient
import pymongo

def dot_product(a, b):
    return sum([a[i]*b[i] for i in range(len(a))])

from numpy import matrix
from numpy import linalg
A = matrix( [[0.4,0.2,0.4],[0.05,0.9,0.05],[0.5,0.4,0.1]]) # Creates a matrix.
x = matrix( [[213.0],[51.0],[90.0]] )                  # Creates a matrix (like a column vector).
y = matrix( [[1,2,3]] )                      # Creates a matrix (like a row vector).
                                 # Inverse of A
print linalg.solve(A, x)
print matrix([0.3,0.4,0.3])*linalg.solve(A, x)     # Solve the linear equation system.