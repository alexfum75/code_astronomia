import math

from scipy.spatial import distance


def pythagoras(vector_a, vector_b):
    dst = distance.euclidean(vector_a, vector_b)
    return dst


def norma(v):
    (x, y, z) = v
    module = (x * x) + (y * y) + (z * z)
    return math.sqrt(module)
