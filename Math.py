from math import *

# Max Trinter, Pascal Mehnert
# 22.04.2016
# Collection of mathematical functions
# V 1.1

pi = math.pi
e = math.e


def fac(zahl):

    zahl = int(zahl)
    
    for i in range(1,(zahl)):
        zahl *= i

    return zahl

def nueberk(n,k):

    n = int(n)
    k = int(k)

    zaehler = fac(n)

    nenner = fac(k)
    nenner = nenner * fac(n-k)
        
    return(zaehler/nenner)

def binompdf(n,p,k):
    n = int(n)
    k = int(k)

    if(k > n):
        print("Error. N <= k!")
        return 0

    if (p > 1):
        print("Error. p <= 1!")

    return (nueberk(n,k)*pow(p,k)*pow((1-p),(n-k)))

def binomcdf(n,p,k):

    n = int(n)
    k = int(k)

    if(k > n):
        print("Error. N <= k!")
        return 0

    if (p > 1):
        print("Error. p <= 1!")


    ergebnis = 0
    for i in range(1,(k+1)):
        ergebnis += binompdf(n,p,i)

    return (ergebnis)

def dec(zaehler,nenner):
    return zaehler/nenner

def frac(zahl):
 
    zaehler = 1
    
    nachkommastellen = len(str(zahl % 1).split(".")[1])

    zaehler = zahl * pow(10,nachkommastellen)

    nenner = pow(10,nachkommastellen)

    rest = 1
    b = zaehler
    a = nenner
    
    while rest != 0:
        rest = b % a
        b = a
        a = rest

    zaehler = int(zaehler/b)
    nenner = int(nenner/b)

    #Hier die Return-Anweisung
    print(zaehler,"/",nenner)


def cos(x):
    return math.cos(x)


def acos(x):
    return math.acos(x)


def acosh(x):
    return math.acosh(x)


def sin(x):
    return math.sin(x)


def asin(x):
    return math.asin(x)


def asinh(x):
    return math.asinh(x)


def tan(x):
    return math.tan(x)


def atan(x):
    return math.atan(x)


def atan2(y, x):
    return math.atan2(y, x)


def atanh(x):
    return math.atanh(x)


def radians(x):
    return (winkel / 360) * (2*pi)


def degrees(x):
    return (winkel * 360) / (2*pi)


def sqrt(x):
    return math.sqrt(x)


def log(x, base):
    return math.log(x, base=base)


def log2(x):
    return math.log2(x)


def log10(x):
    return math.log10(x)


def ln(x):
    return math.log(x, base=math.e)


def factorial(x):
    return math.factorial(x)


def max(a, b):
    return max(a, b)


def abs(x):
    if(x >= 0):
        return x
    else:
        return -x
