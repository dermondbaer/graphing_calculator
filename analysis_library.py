# Max T.
# 19.05.2016
# Collection of analysis functions, using decimals.
# V 1.0

import math_calculator as c
from decimal import *


def nderiv(expression, value):
    epsilon = pow(Decimal(2), -128)

    left_value = c.Calculator.calculate_function_value(expression, {'x': (value - epsilon)})
    right_value = c.Calculator.calculate_function_value(expression, {'x': (value + epsilon)})

    return (right_value - left_value) / (2 * epsilon)


def fnint(expression, left_bound, right_bound):
    swapped = False
    if left_bound > right_bound:
        left_bound, right_bound = right_bound, left_bound
        swapped = True

    epsilon = pow(Decimal(2), -6)
    current = left_bound
    index = 0
    total = Decimal()

    while current < right_bound:
        total += c.Calculator.calculate_function_value(expression, {'x': current})
        index += 1
        current += epsilon

    total = (total / index) * (right_bound - left_bound)

    if swapped:
        total = -total

    return total
