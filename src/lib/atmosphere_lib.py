#!/bin/python3
# -*- coding: utf8 -*- 
"""
@Author : Pierre VAUDRY 
Release date: 20/11/2022

[Description]

    Ce module apporte les calcules de base dans l'atmosphere. 
    Il permet de rendre moins lours en terme de lecture le code python principale.

"""
#############################################
# --------- Import module section --------- #
#############################################

from math import sqrt, pow

#############################################
# ----------- Function section ------------ #
#############################################

def temperature(z:float):
    return 288.15 - (6.5 * 10**-3 * z)  

def pressure(z:float):
    return 101325 * pow((1 - 22.557 * 10**-6 * z), 5.226)

def density(P:float,T:float):
    return P/(287.05 * T)

def sound_speed(T:float):
    return sqrt((1.4 * 287.05 * T))

def Mach_number(v:float,a:float):
    return v/a

def kelvin2celcius(K:float):
    return K - 273.15

def celcius2kelvin(C:float):
    return C + 273.15

def m2feet(z:float):
    return z * 3.2808 

def feet2m(z:float):
    return 0.3048 * z
    
if __name__ == '__main__':
    
    # Run the program
    pass
