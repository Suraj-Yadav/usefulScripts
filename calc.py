from math import *
from math import factorial as fact

# def fact(n):
	# return factorial(n)


def nCr(n, r):
	return fact(n) // (fact(r) * fact(n - r))


def nPr(n, r):
	return fact(n) // fact(n - r)
