#!/bin/python3
# -*- coding: utf8 -*- 
"""
@Author : Pierre VAUDRY 
Release date: 20/11/2022

[Description]

    Ce DM a pour but d'approfondir l’étude du Cessna Citation Mustang vu en TDs.
    Ce programme permet de lancer les exercices selon l'utilisateur.
    Dans la console, renseignez le numero de l'exercice. 
    
    1. DECOLLAGE
        1. Calculer la distance de décollage. | Commande: > 1
        
    2. MONTEE
        1. Calculer la poussée requise. | Commande: > 2.1
        2. Calculer :
            - la poussée,
            - la pente et le taux de montée ainsi obtenus. Exprimer le taux de montée en ft/min 
            Commande: > 2.2
        3. Calculer la poussée nécessaire et la pente de montée. | Commande: > 2.3
        
    3. VOL STABILISE EN CROISIERE
    
    On cherche désormais à étudier les caractéristiques de l’avion en croisière.
    Sur Excel, tracer les courbes suivantes :
    
        1. L’enveloppe de vol avec le plafond de sustentation | Commande: > 3.1
        2. Le domaine de vol | Commande: > 3.2
        3. La poussée requise en fonction de l’altitude pour conserver une vitesse de 165 𝑚/s | Commande: > 3.3
        4. L’endurance en fonction de la vitesse à 10 000 m et avec la consommation spécifique Cs = 0,093 kg/N.h | Commande: > 3.4
        5. Le rayon d’action en fonction de la vitesse à 10 000 m et avec la consommation spécifique Cs = 0,093 kg/N.h | Commande: > 3.5
        
    4. VIRAGE
    
    L’avion est maintenant en virage à 4 500 ft et V = 150 kts = 81 𝑚/s.
    Sur Excel, tracer les courbes suivantes :
    
        1. La poussée requise en fonction de l’inclinaison afin de conserver la vitesse | Commande: > 4.1
        2. La vitesse de décrochage pour chaque cran de volets en fonction de l’inclinaison | Commande: > 4.2

[Class]

    MainApp() -- main class to make first page and instance all functions


[Other variable]:

    Many other constants and variable may be defined;
    these may be used in calls

"""
#############################################
# --------- Import module section --------- #
#############################################

import math
import src.lib.atmosphere_lib as atmo
import src.data.data as dt
import src.lib.aero_formula as aef


def run_1():
    
    temperature = atmo.temperature(atmo.feet2m(dt.z_airport))
    pression = atmo.pressure(atmo.feet2m(dt.z_airport))
    Lr = aef.Bearing_length(dt.v_lof_ms, dt.g, dt.F0, dt.mass_max, dt.r)
    rho = atmo.density(pression, temperature)
    Lenvole = aef.flight_distance(dt.mass_max, dt.g, aef.V2(aef.V_stol(dt.mass_max,dt.g,rho,dt.S,dt.Cz_max)),
                                  dt.v_lof_ms,dt.F(1,atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)),
                                                                  atmo.temperature(atmo.feet2m(dt.z_airport)))),f=(dt.Cz_max/dt.Cx(dt.Cz_max)))
    
    print("Distance de roulage : {} m".format(Lr))
    print("Distance d'envole : {} m".format(Lenvole))
    print("La distance de décollage est {}m.".format(Lr + Lenvole))     
        

def run_2_1():
    # Vsin(gamma) = 3000 ft/min
    # V = 88 m/s => 
    monte = atmo.feet2m(dt.v_z)
    monte /= 60
    print("Montée (m/s) : ", monte)
    
    sin_gamma = monte/dt.v
    gamma = math.asin(sin_gamma)
    gamma_deg = math.degrees(gamma)
    print("Gamma (degrée): ", gamma_deg)
    print("Sin Gamma : ", sin_gamma)
    rho_moyen = (atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)), atmo.temperature(atmo.feet2m(dt.z_airport))) + 
                 atmo.density(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350)))) / 2
    print("Rho : ", rho_moyen)
    poussee_requise = aef.Tu(rho_moyen, dt.S, dt.v, dt.Cx(dt.Cz(math.radians(gamma_deg))), dt.mass_max, dt.g, math.radians(gamma_deg))
    print("Poussée requise : ", poussee_requise)
        
    
def run_2_2():
    rho_moyen = (atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)), atmo.temperature(atmo.feet2m(dt.z_airport))) + 
                 atmo.density(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350)))) / 2
    print("Rho : ", rho_moyen)
    Tu = dt.F(1, rho_moyen)
    finesse_max = aef.finesse_max(dt.k, dt.Cx0)
    print("Finesse max : ", finesse_max)
    Vz = aef.V(dt.v, Tu, dt.mass_max, dt.g, finesse_max)
    print("Vitesse verticale : ", Vz)
    sin_gamma = aef.sin_gamma(Vz, dt.v)
    print("Valeur de sin gamma : ", sin_gamma)
    gamma = math.degrees(math.asin(sin_gamma))
    print("Valeur de gamma : ", gamma)
    
    Taux_montee = Vz * 60
    Taux_montee = atmo.m2feet(Taux_montee)
    print("Taux de montee : ", Taux_montee)


def run_2_3():
    rho_moyen = (atmo.density(atmo.pressure(atmo.feet2m(dt.z_panne)), atmo.temperature(atmo.feet2m(dt.z_panne))) + 
                 atmo.density(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350)))) / 2
    print("Rho : ", rho_moyen)
    Tu_panne = dt.F(1, rho_moyen) / 2
    print("Poussée utile : ", Tu_panne)
    
    poussee_necessaire = aef.Fn(rho_moyen, dt.S, dt.V_enr_ms, dt.Cx(aef.Cz(dt.V_enr_ms,rho_moyen,dt.S,dt.mass_max,dt.g)))
    print("Poussee necessaire : ", poussee_necessaire)
    
    finesse_max = aef.finesse_max(dt.k, dt.Cx0)
    print("Finesse max : ", finesse_max)
    Vz = aef.V(dt.v, Tu_panne, dt.mass_max, dt.g, finesse_max)
    print("Vitesse verticale : ", Vz)
    sin_gamma = aef.sin_gamma(Vz, dt.v)
    print("Valeur de sin gamma : ", sin_gamma)
    gamma = math.degrees(math.asin(sin_gamma))
    print("Valeur de gamma : ", gamma)
    
    Taux_montee = Vz * 60
    Taux_montee = atmo.m2feet(Taux_montee)
    print("Taux de montee : ", Taux_montee)
    


if __name__ == '__main__':
    
    # Run the program
    test = input("Appuyez sur entrer ou n'importe quelle touche\n")
    if test == "t":
        
        run_2_3()
        
        loop = False
    else:
        loop = True
        print(__doc__)
    
    while loop:
        user_select = input("\n{}".format("Commande: > "))
        
        if user_select == '1':
            run_1()
        elif user_select == '2.1': 
            run_2_1()
        elif user_select == '2.2':
            run_2_2()
        elif user_select == '2.3':
            run_2_3()
        elif user_select == '3.1':
            pass
        elif user_select == '3.2':
            pass
        elif user_select == '3.3':
            pass
        elif user_select == '3.4':
            pass
        elif user_select == '3.5':
            pass
        elif user_select == '4.1':
            pass
        elif user_select == '4.21':
            pass
        elif user_select == 'quit':
            quit()
        
        else:
            print("ERREUR de saisie !!!")
        
        
        
        
        