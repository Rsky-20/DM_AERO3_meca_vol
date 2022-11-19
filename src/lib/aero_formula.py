#!/bin/python3
# -*- coding: utf8 -*- 
"""
@Author : Pierre VAUDRY 
Release date: 20/11/2022

[Description]

    Ce module a pour but de permettre d'alléger le code principale permettant une meilleur lecture. 


"""
#############################################
# --------- Import module section --------- #
#############################################

import sys
import pathlib
import math 
import numpy as np

#############################################
# ----------- Function section ------------ #
#############################################

# [1] Decollage

def V_stol(m:float, g:float, rho:float, S:float, Cz_max:float):
    """Fonction permettant de calculer les vitesses de décrochage

    Args:
        m (float): masse
        g (float): constante gravité
        rho (float): masse volumique
        S (float): surface allaire
        Cz_max (float): coefficient de portance

    Returns:
        float: retourne la valeur de la vitesse STOL
    """    
    return math.sqrt((2 * m * g) / (rho * S * Cz_max))

def Bearing_length(V_lof:float, g:float, Fu:float, m:float, r:float):
    """Fonction permettant de calculer la distance
    de roulement sur la piste

    Args:
        V_lof (float): vitesse lift off
        g (float): constante gravité
        Fu (float): Force utile
        m (float): masse
        r (float): coefficient de résistance de la piste

    Returns:
        float: retourne la distance de roulement 
    """    
    return V_lof**2 / ( g * ((Fu / (m * g)) - r))

def V2(V_stol:float):
    """Fonction permettant de calculer la vitesse V2

    Args:              
        V_stol (float): vitesse de décrochage

    Returns:
        float: retourne la vitesse V2
    """    
    return 1.2 * V_stol

def flight_distance(m:float, g:float, V2:float, V_lof:float, Fu:float, f:float):
    """Fonction permettant de calculer la distance d'envole

    Args:
        m (float): masse
        g (float): constante gravité
        V2 (float): vitesse v2
        V_lof (float): vitesse lift off
        Fu (float): poussée utile
        f (float): finesse

    Returns:
        float: retourne la longueur d'envole
    """    
    return ((10.5) + ((V2**2 - V_lof**2) / 2 * g )) / ((Fu / m * g) - (1 / f))

# [2] Decollage

def Tu(rho:float, S:float, V:float, Cx:float, m:float, g:float, gamma:float):
    """Fonction permettant de calculer la poussée utile 

    Args:
        rho (float): masse volumique
        S (float): surface allaire
        V (float): vitesse
        Cx (float): polaire de l'avion
        m (float): masse max de l'avion
        g (float): constante de gravité
        gamma (float): angle d'incidence

    Returns:
        float: retourne la poussée utile
    """    
    return ((1/2) * rho * S * (V**2) * Cx) + (m * g * math.sin(gamma))

def Rx(Tu:float, m:float, g:float, gamma:float):
    """Fonction permettant de calculer la poussée nécessaire

    Args:
        Tu (float): poussée utile
        m (float): masse max de l'avion
        g (float): constante de gravité
        gamma (float): angle d'incidence

    Returns:
        float: retourne la poussée nécessaire
    """    
    return Tu - m * g * math.sin(gamma)


def Rx_(Tu:float, m:float, g:float, Vz:float, V:float):
    """Fonction permettant de calculer la poussée nécessaire

    Args:
        Tu (float): poussée utile
        m (float): masse max de l'avion
        g (float): constante de gravité
        Vz (float): vitesse verticale
        V (float): vitesse de l'avion

    Returns:
        float: retourne la poussée nécessaire
    """     
    return Tu - m * g * (Vz / V)


def sin_gamma(Vz:float, V:float): #= Vz/V
    """Fonction permettant de calculer le sin gamma à 
    partir de la vitesse verticale et de la vitesse 

    Args:
        Vz (float): Vitesse verticale
        V (float): Vitesse
        

    Returns:
        float: retourne le sin gamma
    """    
    return Vz / V


def sin_gamma_(Fu:float, Fn:float, m:float, g:float): #= Vz/V
    """Fonction permettant de calculer le sin gamma

    Args:
        Fu (float): poussée utile max
        Fn (float): poussée nécessaire
        m (float): masse max de l'avion
        g (float): constante de gravité

    Returns:
        float: retourne le sin gamma
    """    
    return (Fu - Fn) / (m * g)

"""

    Fu - Fn     Vz
    ------- = ------ ==> (Fu - Fn) * V = Vz * m * g
     m * g      V


    => (Fu - Fn) /  m * g = sin(gamma)

"""


def finesse_max(k:float, Cx0:float):
    """Fonction permettant de calculer la finesse 
    Maximum

    Args:
        k (float): le coefficient de trainée induite
        Cx0 (float): le Cx0 de la polaire

    Returns:
        float: la valeur de la finesse max
    """    
    return (1/2) * math.sqrt(1/(k * Cx0))

def Fn(rho:float,S:float,V:float,Cx:float):
    """Fonction permettant de calculer la poussée nécessaire

    Args:
        rho (float): masse volumique
        S (float): surface allaire
        V (float): vitesse
        Cx (float): polaire de l'avion

    Returns:
        float: retourn la poussée nécessaire
    """    
    return (1/2) * rho * S * V**2 * Cx

def V_z(V:float, Fu:float, m:float, g:float, finesse_max:float):
    """Fonction permettant de calculer la vitesse verticale de
    l'avion

    Args:
        V (float): vitesse
        Fu (float): poussée utile
        m (float): masse maximum de l'avion
        g (float): constante de gravité
        finesse_max (float): finesse maximale

    Returns:
        float: retourne la vitesse verticale de l'avion
    """    
    return V * ((Fu / (m * g))- (1 / finesse_max))


def Cz(V:float, rho:float, S:float, m:float, g:float):
    """Fonction permettant de calculer Cz

    Args:
        V (float): vitesse de l'avion
        rho (float): masse volumique
        S (float): surface allaire
        m (float): masse de l'avion
        g (float): constante de gravité

    Returns:
        float: retourne la valeur de Cz
    """    
    return (2 * m * g) / (math.pow(V, 2) * rho * S)


# [3] VOL STABILISE EN CROISIERE

def Cz_vmax(k:float, Tu_max:float, m:float, g:float, Cx0:float):
    """Fonction permettant de calculer Cz pour la vitesse maximum

    Args:
        k (float): le coefficient de trainée induite
        Tu_max (float): poussée max
        m (float): masse de l'avion
        g (float): constante de gravité
        Cx0 (float): le Cx0 de la polaire

    Returns:
        float: retourn la valeur de Cz à vmax
    """    
    return (1 / (2 * k )) * ((Tu_max / (m * g)) - math.sqrt((Tu_max / (m * g))**2 - (4 * k * Cx0)))

def V_max(m:float, g:float, rho:float, S:float, Cz_vmax:float):
    """Fonction permettant de calculer les vitesses maximum

    Args:
        m (float): masse de l'avion
        g (float): constante gravité
        rho (float): masse volumique
        S (float): surface allaire
        Cz_vmax (float): coefficient de portance maximumS

    Returns:
        float: retourne la valeur de la vitesse STOL
    """    
    return math.sqrt((2 * m * g) / (rho * S * Cz_vmax))

def Vdec(m:float,g:float,rho:float,S:float,Cz:float) :
    """_summary_

    Args:
        m (float): masse de l'avion
        g (float): constante de gravité
        rho (float): masse volumique
        S (float): surface allaire
        Cz (float): coefficient de portance

    Returns:
        float: retourne la vitesse de décrochage
    """    
    return np.sqrt((2 * m * g) / (rho * S * Cz))

def endurance(m:float, g:float, Cz:float, Cx:float) :
    """Fonction permettant de calculer l'endurance de l'avion

    Args:
        m (float): masse de l'avion
        g (float): constante de gravité
        Cz (float): constante de portance
        Cx (float): polaire de l'avion

    Returns:
        float: retourne la valeur de l'endurance
    """    
    return (150000 * Cz * math.log((m * g) / (2810 * g))) / (g * Cx)

def radius_action(m:float, g:float, S:float, rho:float, Cz:float, Cx:float) :
    """Fonction permettant de calculer le rayon d'action de l'avion

    Args:
        m (float): masse de l'avion
        g (float): constante de gravité
        S (float): surface allaire
        rho (float): masse volumique
        Cz (float): coefficient de portance
        Cx (float): polaire de l'avion

    Returns:
        float: retourne la valeur du rayon d'action de l'avion
    """    
    return (150000 * 2 * (math.sqrt(m * g) - math.sqrt(2810 * g)))*(math.sqrt((2 * Cz) / (rho * S)))/(Cx * g)  
    
def facteur(phi_deg:float) :
    """Fonction permettant de calculer le facteur de charge de l'avion en fonction de l'inclinaison

    Args:
        phi_deg (float): angle virage

    Returns:
        float: retourne la valeur du facteur de charge en fonction de l'angle
    """    
    return 1 / math.cos(math.radians(phi_deg))

def Fv(n:float, rho:float, V:float, Cx:float, S:float):
    """Fonction permettant de calculer la poussée en fonction du virage

    Args:
        n (float): facteur de charge
        rho (float): masse volumique
        V (float): vitesse
        Cx (float): polaire de l'avion
        S (float): surface allaire

    Returns:
        float: retourne la force de poussée en fonction du virage
    """    
    return (1/2) * n * rho * S * V**2 * Cx

def Vdec(m:float, g:float, S:float, rho:float, Cz:float) :
    """Fonction permettant de calculer la vitesse de décrochage

    Args:
        m (float): masse de l'avion
        g (float): constante de gravité
        S (float): surface allaire
        rho (float): masse volumique
        Cz (float): coefficient de portance

    Returns:
        float: retourne la valeur de la vitesse de décrochage
    """    
    return np.sqrt((2* m * g)/(rho * S * Cz))

def Vn(n:float,Vdec:float):
    """Fonction permettant de calculer la vitesse en fonction du facteur de charge

    Args:
        n (float): facteur de charge
        Vdec (float): vitesse de décrochage

    Returns:
        float: retourne la valeur de la vitesse en fonction du facteur de charge
    """    
    return Vdec * math.sqrt(n)

if __name__ == '__main__':
    # Run the program
    pass
