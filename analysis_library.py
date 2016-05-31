# Pascal Mehnert
# 19.05.2016
# Collection of differential functions, using decimals.
# V 0.1

import math_calculator as c
from decimal import *


def nderiv(expression, value):
    epsilon = pow(Decimal(2), -128)

    left_value = c.Calculator.calculate_function_value(expression, {'x': (value - epsilon)})
    right_value = c.Calculator.calculate_function_value(expression, {'x': (value + epsilon)})

    return (right_value - left_value) / (2 * epsilon)


def fnint(expression, left, right):
    swapped = False
    if left > right:
        left, right = right, left
        swapped = True

    epsilon = pow(Decimal(2), -8)
    current = left
    index = 0
    total = Decimal()

    while current < right:
        total += c.Calculator.calculate_function_value(expression, {'x': current})
        index += 1
        current += epsilon

    total = (total / index) * (right - left)

    if swapped:
        total = -total

    return total
