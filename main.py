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

[Fonction]




[Autres variables]:


"""
#############################################
# --------- Import module section --------- #
#############################################
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import src.lib.atmosphere_lib as atmo
import src.data.data as dt
import src.lib.aero_formula as aef

#############################################
# ----------- Function section ------------ #
#############################################

def run_1():
    
    temperature = atmo.temperature(atmo.feet2m(dt.z_airport))
    pression = atmo.pressure(atmo.feet2m(dt.z_airport))

    Lr = aef.Bearing_length(dt.v_lof_ms, dt.g, dt.F0, dt.mass_max, dt.r)
    rho = atmo.density(pression, temperature)
    print("""
La température (pour z = 1900 feet) est : {}
La pression (pour z = 1900 feet) est : {}
La densité (pour z = 1900 feet) est : {} 
La Vitesse V2 (pour z = 1900 feet) est : {}
La Vitesse Vstol de décrochage (pour z = 1900 feet) est : {}
La Poussé Tu (pour z = 1900 feet) est : {}
          """.format(temperature, pression, rho, aef.V2(aef.V_stol(dt.mass_max,dt.g,rho,dt.S,dt.Cz_max)), 
                     aef.V_stol(dt.mass_max,dt.g,rho,dt.S,dt.Cz_max), 
                     dt.F(1,atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)),
                                         atmo.temperature(atmo.feet2m(dt.z_airport)))),f=(dt.Cz_max/dt.Cx(dt.Cz_max))))
    
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
    print("\nMontée (m/s) : ", monte)
    
    sin_gamma = monte/dt.v
    gamma = math.asin(sin_gamma)
    gamma_deg = math.degrees(gamma)
    print("Gamma (degrée): ", gamma_deg)
    print("Sin Gamma : ", sin_gamma)
    print("""
Pression à 1900 feet : {}
Temerature à 1900 feet : {}
          """.format(atmo.pressure(atmo.feet2m(dt.z_airport)), atmo.temperature(atmo.feet2m(dt.z_airport))))
    print("""
Pression à FL350 feet : {}
Temerature à FL350 feet : {}
          """.format(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350))))
    rho_moyen = (atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)), atmo.temperature(atmo.feet2m(dt.z_airport))) + 
                 atmo.density(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350)))) / 2
    print("Cz = ", dt.Cz_2(dt.mass_max,dt.g,gamma,rho_moyen,dt.S,dt.v))
    print("Cx = ", dt.Cx(dt.Cz_2(dt.mass_max,dt.g,gamma,rho_moyen,dt.S,dt.v)))
    print("Rho à 1900 feet : ", atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)), atmo.temperature(atmo.feet2m(dt.z_airport))))
    print("Rho à FL350 : ", atmo.density(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350))))
    print("Rho moyen : ", rho_moyen)
    poussee_requise = aef.Tu(rho_moyen, dt.S, dt.v, dt.Cx(dt.Cz_2(dt.mass_max,dt.g,gamma,rho_moyen,dt.S,dt.v)), dt.mass_max, dt.g, gamma)
    print("Poussée requise : ", poussee_requise)
        
    
def run_2_2():
    rho_moyen = (atmo.density(atmo.pressure(atmo.feet2m(dt.z_airport)), atmo.temperature(atmo.feet2m(dt.z_airport))) + 
                 atmo.density(atmo.pressure(atmo.feet2m(dt.FL350)), atmo.temperature(atmo.feet2m(dt.FL350)))) / 2
    print("Rho : ", rho_moyen)
    Tu = dt.F(1, rho_moyen)
    print("Poussée : ",Tu)
    finesse_max = aef.finesse_max(dt.k, dt.Cx0)
    print("Finesse max : ", finesse_max)
    Vz = aef.V_z(dt.v, Tu, dt.mass_max, dt.g, finesse_max)
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
    Vz = aef.V_z(dt.v, Tu_panne, dt.mass_max, dt.g, finesse_max)
    print("Vitesse verticale : ", Vz)
    sin_gamma = aef.sin_gamma(Vz, dt.v)
    print("Valeur de sin gamma : ", sin_gamma)
    gamma = math.degrees(math.asin(sin_gamma))
    print("Valeur de gamma : ", gamma)
    
    Taux_montee = Vz * 60
    Taux_montee = atmo.m2feet(Taux_montee)
    print("Taux de montee : ", Taux_montee)
    


def run_3_1():
    def flight_envelope():
        
        Altitude = np.linspace(0, 13300, 175)
        T, P, rho, V_min, V_max = [], [], [], [], []


        for i in Altitude:
            T.append(atmo.temperature(i))
            P.append(atmo.pressure(i))


        for i in range(len(T)):
            rho.append(atmo.density(P[i], T[i]))

        for i in range(len(Altitude)):
            V_min.append((aef.V_stol(dt.mass_max,dt.g,rho[i],dt.S,dt.Cz_max)))
            V_max.append(aef.V_max(dt.mass_max,dt.g,rho[i],dt.S,aef.Cz_vmax(dt.k, dt.F(1, rho[i]),dt.mass_max, dt.g, dt.Cx0)))

        V_min = np.array(V_min)

        graph = plt.subplot(111)
        graph.plot(V_min, Altitude, label = "Vitesse min", color = "blue")
        graph.plot(V_max, Altitude, label = "Vitesse max", color = "red")

        x = np.linspace(V_min[-1], V_max[-1], 175)
        y = []
        for _ in range(175):
            y.append(13300)

        graph.plot(x, y, label = "Plafond de sus", color = "black")

        graph.set_xlabel("Vitesse de l'avion (m/s)")
        graph.set_ylabel("Altitude (m)")
        graph.set_title("Question 1 - Enveloppe de vol")

        graph.fill_between(V_min, Altitude, where = V_min <= V_min[-1], facecolor = "yellow", label = "Zone de vol")
        graph.fill_between(x, y, where = (x >= float(V_min[-1])) & (x <= V_max[0]), facecolor = "yellow")
        graph.fill_between(V_max, y, where = (V_max >= V_max[0]) & (V_max <= V_max[-1]), facecolor = "yellow")
        graph.fill_between(V_max, Altitude, where = (V_max >= V_max[0]) & (V_max <= V_max[-1]), facecolor = "white")
        

        dot = Ellipse( (V_min[0], 0), width = 5, height = 500, edgecolor = "black")
        dot.set_facecolor("black")
        graph.add_patch(dot)
        graph.text(V_min[0] - 10, -500, f'V = {str(V_min[0])[0:6]}m/s')

        dot = Ellipse( (V_min[-1], 13300), width = 5, height = 500, edgecolor = "black")
        dot.set_facecolor("black")
        graph.add_patch(dot)
        graph.text(V_min[-1] - 30, 13300 - 700, f'V = {str(V_min[-1])[0:6]}m/s')

        dot = Ellipse( (V_max[-1], 13300), width = 5, height = 500, edgecolor = "black")
        dot.set_facecolor("black")
        graph.add_patch(dot)
        graph.text(V_max[-1] + 10, 13300, f'V = {str(V_max[-1])[0:6]}m/s')

        dot = Ellipse( (V_max[0], 0), width = 5, height = 500, edgecolor = "black")
        dot.set_facecolor("black")
        graph.add_patch(dot)
        graph.text(V_max[0] - 10, -500, f'V = {str(V_max[0])[0:6]}m/s')

        #print(V_min[0], V_min[-1], V_max[0], V_max[-1])

        graph.grid(True)
        graph.legend(loc = "upper left")
        plt.show()
        
            
            
    flight_envelope() 


if __name__ == '__main__':
    
    # Run the program
    test = input("Appuyez sur entrer ou n'importe quelle touche\n")
    if test == "t":
        
        run_3_1()
        
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
        
        
        
        
        