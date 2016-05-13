# Max T., Pascal Mehnert
# 13.05.2016
# Collection of mathematical functions
# V 1.1

import math
import builtins

pi = math.pi
e = math.e
epsilon = pow(10,-16)


def cos(x):
    """Returns the cosine of x (measured in radians)."""
    return math.cos(x)


def cosh(x):
    """Returns the hyperbolic cosine of x."""
    return math.cosh(x)


def acos(x):
    """Returns the arc sine of x (measured in radians)."""
    return math.acos(x)


def acosh(x):
    """Returns the reverse hyperbolic cosine of x."""
    return math.acosh(x)


def sin(x):
    """Returns the sine of x (measured in radians)."""
    return math.sin(x)


def sinh(x):
    """Returns the hyperbolic sine of x."""
    return math.sinh(x)


def asin(x):
    """Returns the arc sine of x (measured in radians)."""
    return math.asin(x)


def asinh(x):
    """Returns the reverse hyperbolic sine of x."""
    return math.asinh(x)


def tan(x):
    """Returns the tangent of x (measured in radians)."""
    return math.tan(x)


def tanh(x):
    """Returns the hyperbolic tangent of x."""
    return math.tanh(x)


def atan(x):
    """Returns the arc tangent of x (measured in radians)."""
    return math.atan(x)


def atan2(y, x):
    """Returns the arc tangent of x/y (measured in radians)."""
    return math.atan2(y, x)


def atanh(x):
    """Returns the reverse hyperbolic tangent of x."""
    return math.atanh(x)


def radians(x):
    """Converts the angle x from degrees to radians and returns it."""
    return (x/360)*2*pi


def degrees(x):
    """Converts the angle x from radians to degrees and returns it."""
    return x*360/(2*pi)


def sqrt(x):
    """Returns the square root of x."""
    i = 1
    y = x
    r = x
    l = x/2
    while i >= epsilon:
        res = pow(l,2)
        if(res>y):
            i = res-y
            r = l
            l = l/2
        elif(res<y):
            i = y-res
            l = l + 0.5*(r-l)
        else:
            i=0
    return l


def log(x, base):
    """Returns the logarithm of x to the base of base."""
    
    return math.log(x, n)


def log2(x):
    """Returns the logarithm of x to the base of 2."""
    return math.log2(x)


def log10(x):
    """Returns the logarithm of x to the base of 10."""
    return math.log10(x)


def ln(x):
    """Returns the natural logarithm of x."""
    return math.log(x, math.e)


def factorial(x):
    """Returns the factorial of n."""
    for i in range(1,x):
        x *= i

    return x


def max(a, b):
    """Returns the maximum of a and b."""
    if(a>b):
        return a
    else:
        return b


def min(a, b):
    """Returns the minimum of a and b."""
    if(a<b):
        return a
    else:
        return b

def abs(x):
    """Returns the absolute of x."""
    if(x<0):
        return -x
    else:
        return x


def binompdf(n, p, k):
    """
    Returns the probability for exactly k successes in a binomially distributed random experiment.

    :param n: The number of independent trials.
    :param p: The probability for a success.
    :param k: The number of successes.
    :return: The probability for k successes.
    """
    if k > n:
        raise ValueError('K must not be greater than N.')
    if n < 1:
        raise ValueError('N must not be smaller than 1.')
    if p > 1:
        raise ValueError('Probability must not be greater than one.')
    if p < 0:
        raise ValueError('Probability must not be smaller than one.')

    return ncr(n, k) * pow(p, k) * pow((1 - p), (n - k))


def binomcdf(n, p, k):
    """
    Returns the probability for k or less successes in a binomially distributed random experiment.

    :param n: The number of independent trials.
    :param p: The probability for a success.
    :param k: The number of succeeds.
    :return: The probability for at least k successes.
    """
    k = int(k)
    n = int(n)
    if k > n:
        raise ValueError('K must not be greater than N.')
    if n < 1:
        raise ValueError('N must not be smaller than 1.')
    if p > 1:
        raise ValueError('Probability must not be greater than one.')
    if p < 0:
        raise ValueError('Probability must not be smaller than one.')

    result = 0
    for i in range(0, (k + 1)):
        result += binompdf(n, p, i)

    return result


def ncr(n, k):
    """Returns the combination of n and k."""
    n = int(n)
    k = int(k)
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n - k)

    return numerator / denominator


def npr(n, k):
    """Returns the permutation of n and k."""
    n = int(n)
    k = int(k)
    numerator = factorial(n)
    denominator = factorial(k)

    return numerator / denominator


print(log(3,5))
