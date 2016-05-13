import math
from math_calculator import Calculator
from math_calculator import *


def nderiv(expression,variable, value):

    epsilon = pow(2,-32)
    
    wertL = Calculator.calculate_function_value(expression, {variable:(value-epsilon)})
    wertR = Calculator.calculate_function_value(expression, {variable:(value+epsilon)})
    
    return ((wertR-wertL)/(2*epsilon))


def fnInt(expression, left, right, variable):

    epsilon = pow(2,-16)

    current = left

    i = 0

    summe = 0

    while current < right:

        wertAktuell = Calculator.calculate_function_value(expression, {variable:current})

        summe += wertAktuell

        i += 1
        
        current += epsilon

    summe = (summe/i)*(right-left)
    
    return round(summe,3)

funktion = "3 * x ^ 2 + 5 * x - 4"
#funktion = "sin ( x )"
#funktion = "ln ( 5 * x )"
#funktion = "x ^ x"
variable = "x"
links = 1
rechts = 3
xwert = 4

function = Calculator.calculate_expression(funktion)

print("Thinkin'...")

print("Funktion ",funktion," nach ",variable,"=",xwert," abgeleitet: ",nderiv(function, variable, xwert), sep="")

print("Thinkin'...")

print("Funktion ",funktion," integriert im Bereich von ",links," nach ",rechts," nach ",variable,": ",fnInt(function,links,rechts, variable),sep="")

