from math import *
from math import factorial as fact
#An init script for python/ipython to be used as a calculator.
# def fact(n):
	# return factorial(n)


def nCr(n, r):
	return fact(n) // (fact(r) * fact(n - r))


def nPr(n, r):
	return fact(n) // fact(n - r)
