"""
Author : Tim Berneiser
Date   : 2024-05-27
Purpose: Functions for mathematical operations
"""

from functools import lru_cache


# --------------------------------------------------
@lru_cache()
def fib(gen, lit):
    """ Recusively calculate Fibonacci sequence """

    litter_size = 0

    if gen <1:
        return 0

    if gen in (1,2):
        return 1

    litter_size = fib(gen-1, lit) + fib(gen-2, lit)*lit

    return litter_size


# --------------------------------------------------
@lru_cache()
def fibd(gen, months, litter=1):
    """ Recusively calculate Fibonacci sequence with mortal rabbits """

    litter_size = 0
    pregnancies = 0

    if gen == 1:
        return [1, 0]
    if gen == 2:
        return [1, litter]
    if gen == 0:
        return [0, 1]
    if gen <= 0:
        return [0, 0]

    for i in range(months+1)[1:]:
        litter_size += fibd(gen-i, months, litter)[1]
    for i in range(months+1)[2:]:
        pregnancies += (fibd(gen-i, months, litter)[1])*litter

    return [litter_size, pregnancies]


# --------------------------------------------------
def dom_prob(k: int, m: int, n: int):

    summed = k + m + n

    prob = 1/summed * (k 
                      + m/2 + (m*k)/(2*(summed-1)) + ((m-1)*m)/(4*(summed-1)) 
                      + (n*k)/(summed-1) + (n*m)/(2*(summed-1)))

    return prob