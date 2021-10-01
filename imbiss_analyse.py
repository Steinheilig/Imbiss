# -*- coding: utf-8 -*-
"""
Analyse der Spielmechanik von 
"Imbiss" v. 5.4 von T. Bauer für IBM PC, Public Domain

Analyse Strategie:
    1) Grundlegende Bestimmung von BK,ZK,EK als Funktion der Temperatur (d.h. keine Einfluss der VKs)
    2) BK,ZK,EK Temperaturabhängigkeit
    3) Bestimmen Parameter zum Preisvergleich innerhalb einer Warengruppe 
       NICHT NOTWENDIG FÜR OPTIMIRUNG PREIS_MAX IN KUNDENVERHALTEN -> nicht analysiert    

Hypothese:
    Cola / Bratwurst Anomalie -> Einfluss der VKs auf Basis des Max wertes der Gruppe 
    -> bestaetigt

Optimale Verkausstrategien ableiten

@author: Steinheilig, 2021
"""

import numpy as np 
import matplotlib.pyplot as plt 



#%%  Zigaretten ZK(V)

### Woche	Tag	Temperatur	 // Preise:// S.Eis	V.Eis	E.Eis	Cola	Zig.	Bratwurst	Fritten	 // Verkauf:// Kunden	S.Eis	V.Eis	E.Eis	Cola	Zig.	Bratwurst	Fritten	G1(Eisgruppe)	G2(Bratwurstgruppe)
data = np.array(
[[1,	1,	12,	0,	0,	0,	0,	50,	0,	0,	10,	0,	0,	0,	0,	16,	0,	0,	0,	0],
[1,	1,	-8,	0,	0,	0,	0,	100,	0,	0,	9,	0,	0,	0,	0,	15,	0,	0,	0,	0],
[1,	2,	8,	0,	0,	0,	0,	150,	0,	0,	9,	0,	0,	0,	0,	13,	0,	0,	0,	0],
[1,	3,	12,	0,	0,	0,	0,	150,	0,	0,	9,	0,	0,	0,	0,	13,	0,	0,	0,	0],
[1,	4,	28,	0,	0,	0,	0,	150,	0,	0,	9,	0,	0,	0,	0,	13,	0,	0,	0,	0],
[1,	1,	34,	0,	0,	0,	0,	150,	0,	0,	9,	0,	0,	0,	0,	14,	0,	0,	0,	0],
[1,	1,	3,	0,	0,	0,	0,	200,	0,	0,	8,	0,	0,	0,	0,	13,	0,	0,	0,	0],
[1,	2,	22,	0,	0,	0,	0,	200,	0,	0,	8,	0,	0,	0,	0,	11,	0,	0,	0,	0],
[1,	3,	29,	0,	0,	0,	0,	200,	0,	0,	8,	0,	0,	0,	0,	11,	0,	0,	0,	0],
[1,	4,	37,	0,	0,	0,	0,	200,	0,	0,	8,	0,	0,	0,	0,	13,	0,	0,	0,	0],
[1,	1,	11,	0,	0,	0,	0,	250,	0,	0,	8,	0,	0,	0,	0,	14,	0,	0,	0,	0],
[1,	2,	27,	0,	0,	0,	0,	300,	0,	0,	7,	0,	0,	0,	0,	11,	0,	0,	0,	0],
[1,	3,	33,	0,	0,	0,	0,	300,	0,	0,	7,	0,	0,	0,	0,	12,	0,	0,	0,	0],
[1,	4,	1,	0,	0,	0,	0,	300,	0,	0,	7,	0,	0,	0,	0,	11,	0,	0,	0,	0],
[1,	5,	11,	0,	0,	0,	0,	350,	0,	0,	7,	0,	0,	0,	0,	8,	0,	0,	0,	0],
[1,	1,	7,	0,	0,	0,	0,	350,	0,	0,	7,	0,	0,	0,	0,	9,	0,	0,	0,	0],
[1,	3,	30,	0,	0,	0,	0,	350,	0,	0,	7,	0,	0,	0,	0,	12,	0,	0,	0,	0],
[1,	4,	-4,	0,	0,	0,	0,	350,	0,	0,	7,	0,	0,	0,	0,	12,	0,	0,	0,	0],
[1,	5,	22,	0,	0,	0,	0,	400,	0,	0,	6,	0,	0,	0,	0,	8,	0,	0,	0,	0],
[1,	1,	9,	0,	0,	0,	0,	400,	0,	0,	6,	0,	0,	0,	0,	8,	0,	0,	0,	0],
[1,	2,	-4,	0,	0,	0,	0,	400,	0,	0,	6,	0,	0,	0,	0,	8,	0,	0,	0,	0],
[1,	3,	6,	0,	0,	0,	0,	450,	0,	0,	6,	0,	0,	0,	0,	9,	0,	0,	0,	0],
[1,	4,	34,	0,	0,	0,	0,	450,	0,	0,	6,	0,	0,	0,	0,	9,	0,	0,	0,	0],
[1,	4,	-5,	0,	0,	0,	0,	450,	0,	0,	6,	0,	0,	0,	0,	9,	0,	0,	0,	0],
[1,	1,	5,	0,	0,	0,	0,	500,	0,	0,	5,	0,	0,	0,	0,	6,	0,	0,	0,	0],
[1,	2,	1,	0,	0,	0,	0,	500,	0,	0,	5,	0,	0,	0,	0,	7,	0,	0,	0,	0],
[1,	3,	32,	0,	0,	0,	0,	550,	0,	0,	5,	0,	0,	0,	0,	9,	0,	0,	0,	0],
[1,	4,	25,	0,	0,	0,	0,	550,	0,	0,	5,	0,	0,	0,	0,	7,	0,	0,	0,	0],
[1,	5,	11,	0,	0,	0,	0,	600,	0,	0,	4,	0,	0,	0,	0,	7,	0,	0,	0,	0],
[1,	1,	4,	0,	0,	0,	0,	600,	0,	0,	4,	0,	0,	0,	0,	7,	0,	0,	0,	0],
[1,	2,	21,	0,	0,	0,	0,	650,	0,	0,	4,	0,	0,	0,	0,	8,	0,	0,	0,	0],
[1,	3,	14,	0,	0,	0,	0,	650,	0,	0,	4,	0,	0,	0,	0,	5,	0,	0,	0,	0],
[1,	4,	33,	0,	0,	0,	0,	700,	0,	0,	3,	0,	0,	0,	0,	4,	0,	0,	0,	0],
[1,	5,	23,	0,	0,	0,	0,	750,	0,	0,	3,	0,	0,	0,	0,	3,	0,	0,	0,	0],
[1,	1,	20,	0,	0,	0,	0,	800,	0,	0,	2,	0,	0,	0,	0,	3,	0,	0,	0,	0],
[1,	2,	25,	0,	0,	0,	0,	850,	0,	0,	2,	0,	0,	0,	0,	3,	0,	0,	0,	0],
[1,	3,	19,	0,	0,	0,	0,	900,	0,	0,	1,	0,	0,	0,	0,	2,	0,	0,	0,	0],
[1,	4,	-8,	0,	0,	0,	0,	950,	0,	0,	1,	0,	0,	0,	0,	2,	0,	0,	0,	0],
[1,	5,	-9,	0,	0,	0,	0,	1000,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,  0]])

estimate = np.zeros([1100,])
V = np.zeros([1100,])
jj = 0 
for V_test in range(0,1100,1):    
    ZK = 10 
    ZK -= int(V_test/100.)
    estimate[jj] = ZK
    V[jj] = V_test
    jj+=1
        
plt.figure()
#plt.plot(data[:,7],data[:,15],'X',color='black')
plt.plot(data[:,7],data[:,10],'X',color='black')
plt.plot(V,estimate,'--',color='black')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Zigaretten Kunden am Wochentag')
ts = str('ZK-=int(V/100)')
plt.legend(['Probe',ts])
plt.show()

#%% Zigaretten SAMSTAG / SONNTAG

data = np.array([
[1,	6,	13,	0,	0,	0,	0,	1,	0,	0,	12,	0,	0,	0,	0,	0,	18,	0,	0,	18],
[1,	6,	31,	0,	0,	0,	0,	1,	0,	0,	12,	0,	0,	0,	0,	0,	19,	0,	0,	19],
[1,	7,	26,	0,	0,	0,	0,	1,	0,	0,	15,	0,	0,	0,	0,	0,	24,	0,	0,	24],
[1,	7,	-7,	0,	0,	0,	0,	1,	0,	0,	15,	0,	0,	0,	0,	0,	25,	0,	0,	25]])

ZK = 12 # Samstags
ZK = 15 # Sonntags
                

#%% Beste Zigarettenstrategie als Funktion des Verkaufspreises
ZKs = np.array([10,12,15])
Erwarteter_Gewinn = np.zeros([1000,])
Preisempfehlung =  np.zeros([3,])
for Wochengruppe in range(3):
    BestGewinn = 0
    for V in range(0,1000):
      Erwarteter_Gewinn[V] = (V-200)*(ZKs[Wochengruppe]-int(V/100))  # 200Pf ist der niedrigste mögliche Einkaufswert -> max Gewinn
      if Erwarteter_Gewinn[V] < 0 :
          Erwarteter_Gewinn[V] = 0 
      if Erwarteter_Gewinn[V] > BestGewinn:
          BestGewinn = Erwarteter_Gewinn[V]
          Preisempfehlung[Wochengruppe] = V

#Preisempfehlung
#Out[69]: array([699., 799., 899.])  # d.h. 699 am Wochentag, 799 am Samstag und 899 am Sonntag! :) 
                

#%% Eiskunden EK(V,T) WOCHENTAG
data = np.array(
[[1,1,	18,	50,	     0,	0,	0,	0,	0,	0,	19,	31,	0,	0,	0,	0,	0,	0,	31,	0],
[1,	2,	-1,	50,	     0,	0,	0,	0,	0,	0,	15,	19,	0,	0,	0,	0,	0,	0,	19,	0],
[1,	3,	-7,	50,  	0,	0,	0,	0,	0,	0,	14,	20,	0,	0,	0,	0,	0,	0,	20,	0],
[1,	4,	-2,	60,  	0,	0,	0,	0,	0,	0,	14,	20,	0,	0,	0,	0,	0,	0,	20,	0],
[1,	5,	12,	70,  	0,	0,	0,	0,	0,	0,	16,	25,	0,	0,	0,	0,	0,	0,	25,	0],
[1,	1,	34,	80,  	0,	0,	0,	0,	0,	0,	20,	29,	0,	0,	0,	0,	0,	0,	29,	0],
[1,	2,	26,	90,  	0,	0,	0,	0,	0,	0,	17,	29,	0,	0,	0,	0,	0,	0,	29,	0],
[1,	3,	13,	100,	0,	0,	0,	0,	0,	0,	13,	22,	0,	0,	0,	0,	0,	0,	22,	0],
[1,	4,	-6,	110,	0,	0,	0,	0,	0,	0,	8,	14,	0,	0,	0,	0,	0,	0,	14,	0],
[1,	5,	26,	120,	0,	0,	0,	0,	0,	0,	15,	21,	0,	0,	0,	0,	0,	0,	21,	0],
[1,	2,	-2,	130,	0,	0,	0,	0,	0,	0,	7,	13,	0,	0,	0,	0,	0,	0,	13,	0],
[1,	3,	25,	130,	0,	0,	0,	0,	0,	0,	13,	18,	0,	0,	0,	0,	0,	0,	18,	0],
[1,	4,	19,	140,	0,	0,	0,	0,	0,	0,	10,	17,	0,	0,	0,	0,	0,	0,	17,	0],
[1,	5,	9,	150,	0,	0,	0,	0,	0,	0,	7,	11,	0,	0,	0,	0,	0,	0,	11,	0],
[1,	2,	30,	160,	0,	0,	0,	0,	0,	0,	11,	16,	0,	0,	0,	0,	0,	0,	16,	0],
[1,	3,	34,	170,	0,	0,	0,	0,	0,	0,	11,	17,	0,	0,	0,	0,	0,	0,	17,	0],
[1,	4,	23,	180,	0,	0,	0,	0,	0,	0,	7,	12,	0,	0,	0,	0,	0,	0,	12,	0],
[1,	5,	19,	190,	0,	0,	0,	0,	0,	0,	5,	6,	0,	0,	0,	0,	0,	0,	6,	0],
[1,	1,	30,	200,	0,	0,	0,	0,	0,	0,	7,	12,	0,	0,	0,	0,	0,	0,	12,	0],
[1,	2,	35,	210,	0,	0,	0,	0,	0,	0,	7,	11,	0,	0,	0,	0,	0,	0,	11,	0],
[1,	3,	37,	220,	0,	0,	0,	0,	0,	0,	7,	13,	0,	0,	0,	0,	0,	0,	13,	0],
[1,	4,	-1,	230,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[1,	5,	20,	230,	0,	0,	0,	0,	0,	0,	2,	4,	0,	0,	0,	0,	0,	0,	4,	0],
[1,	2,	10,	230,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[1,	3,	20,	220,	0,	0,	0,	0,	0,	0,	3,	4,	0,	0,	0,	0,	0,	0,	4,	0],
[1,	4,	23,	230,	0,	0,	0,	0,	0,	0,	2,	4,	0,	0,	0,	0,	0,	0,	4,	0],
[1,	5,	38,	230,	0,	0,	0,	0,	0,	0,	6,	8,	0,	0,	0,	0,	0,	0,	8,	0],
[1,	1,	23,	240,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	1,	0],
[1,	3,	25,	250,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	1,	0],
[1,	4,	30,	260,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	1,	0],
[1,	2,	33,	270,	0,	0,	0,	0,	0,	0,	1,	1,	0,	0,	0,	0,	0,	0,	1,	0],
[1,	4,	33,	280,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0]]
   )


estimate = np.zeros([data.shape[0],])
for jj in range(data.shape[0]):
    TE = data[jj,2]
    EK = 20     
    EK -= int(data[jj,3]/10)   # EK -= int(V/10)
    EK += (int(TE/4))
    if EK < 0:
        EK = 0 
    estimate[jj] = EK
        

plt.figure()
plt.plot(data[:,3],data[:,10],'o',color='black')
plt.plot(data[:,3],estimate,'X',color='red')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Eis Kunden am Wochentag')
plt.show()


#%% Beste Eisstrategie als Funktion der Temperatur
Erwarteter_Gewinn = np.zeros([49,400])
Preisempfehlung =  np.zeros([49,])
for TE in range(-9,40):
    BestGewinn = 0
    for V in range(0,400):
      Erwarteter_Gewinn[TE+9,V] = (20 + int(TE/4) - int(V/10) )*(V-10)  # 10Pf ist der niedrigste mögliche Einkaufswert -> max Gewinn
      if (20 + int(TE/4) - int(V/10) ) < 0 :
          Erwarteter_Gewinn[TE+9,V] = 0 
      if Erwarteter_Gewinn[TE+9,V] > BestGewinn:
          BestGewinn =  Erwarteter_Gewinn[TE+9,V]
          Preisempfehlung[TE+9] = V
    

fig = plt.figure()
plt.imshow(Erwarteter_Gewinn.transpose()/1e2)
plt.plot(Preisempfehlung[0:41],color='white')
plt.plot([40,41,42,43,44,45,46,47,48],Preisempfehlung[40:],color='white')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.1)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.gca().invert_yaxis()
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Eis Strategie -Wochentags-')
cbar = plt.colorbar()
plt.text(55,410,'>=')
plt.clim(-5,30)
cbar.ax.set_ylabel('Erwarteter Gewinn (S=1) [DM]', rotation=90)
plt.savefig('OptimaleEisStrategie.jpg', dpi=600)
plt.show()


#%% EISKUNDEN EK(T,V) SAMSTAG
data = np.array([
[1,	6,	9,	1,	    0,	0,	0,	0,	0,	0,	25,	42,	0,	0,	0,	0,	0,	0,	42,	0],
[1,	6,	0,	100,	0,	0,	0,	0,	0,	0,	15,	24,	0,	0,	0,	0,	0,	0,	24,	0],
[1,	6,	-8,	120,	0,	0,	0,	0,	0,	0,	11,	18,	0,	0,	0,	0,	0,	0,	18,	0],
[1,	6,	-6,	180,	0,	0,	0,	0,	0,	0,	6,	9,	0,	0,	0,	0,	0,	0,	9,	0],
[1,	6,	20,	200,	0,	0,	0,	0,	0,	0,	10,	16,	0,	0,	0,	0,	0,	0,	16,	0],
[1,	6,	17,	220,	0,	0,	0,	0,	0,	0,	7,	9,	0,	0,	0,	0,	0,	0,	9,	0],
[1,	6,	5,	140,	0,	0,	0,	0,	0,	0,	12,	19,	0,	0,	0,	0,	0,	0,	19,	0],
[1,	6,	2,	80,	   0,	0,	0,	0,	0,	0,	17,	28,	0,	0,	0,	0,	0,	0,	28,	0]])

estimate = np.zeros([data.shape[0],])
for jj in range(data.shape[0]):
    TE = data[jj,2]
    EK = 25     
    EK -= int(data[jj,3]/10)   # EK -= int(V/10)
    EK += (int(TE/4))
    if EK < 0:
        EK = 0 
    estimate[jj] = EK        

plt.figure()
plt.plot(data[:,3],data[:,10],'o',color='black')
plt.plot(data[:,3],estimate,'X',color='red')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Eis Kunden am Samstag')
plt.show()


#%% Beste Eisstrategie als Funktion der Temperatur
Erwarteter_Gewinn = np.zeros([49,400])
Preisempfehlung =  np.zeros([49,])
for TE in range(-9,40):
    BestGewinn = 0
    for V in range(0,400):
      Erwarteter_Gewinn[TE+9,V] = (25 + int(TE/4) - int(V/10) )*(V-10)  # 10Pf ist der niedrigste mögliche Einkaufswert -> max Gewinn
      if (25 + int(TE/4) - int(V/10) ) < 0 :
          Erwarteter_Gewinn[TE+9,V] = 0 
      if Erwarteter_Gewinn[TE+9,V] > BestGewinn:
          BestGewinn =  Erwarteter_Gewinn[TE+9,V]
          Preisempfehlung[TE+9] = V
    

fig = plt.figure()
plt.imshow(Erwarteter_Gewinn.transpose()/1e2)
plt.plot(Preisempfehlung[0:41],color='white')
plt.plot([40,41,42,43,44,45,46,47,48],Preisempfehlung[40:],color='white')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.1)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.gca().invert_yaxis()
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Eis Strategie -Samstags-')
plt.text(55,410,'>=')
cbar = plt.colorbar()
plt.clim(-5,30)
cbar.ax.set_ylabel('Erwarteter Gewinn (S=1) [DM]', rotation=90)
plt.savefig('OptimaleEisStrategie_Sa.jpg', dpi=600)
plt.show()


#%% EISKUNDEN EK(T,V) SONNTAG
data = np.array([
[1,	7,	29,	180,	0,	0,	0,	0,	0,	0,	17,	30,	0,	0,	0,	0,	0,	0,	30,	0],
[1,	7,	5,	140,	0,	0,	0,	0,	0,	0,	17,	25,	0,	0,	0,	0,	0,	0,	25,	0],
[1,	7,	-6,	100,	0,	0,	0,	0,	0,	0,	19,	30,	0,	0,	0,	0,	0,	0,	30,	0],
[1,	7,	15,	140,	0,	0,	0,	0,	0,	0,	19,	30,	0,	0,	0,	0,	0,	0,	30,	0],
[1,	7,	8,	80,	0,	0,	0,	0,	0,	0,	24,	36,	0,	0,	0,	0,	0,	0,	36,	0]])


estimate = np.zeros([data.shape[0],])
for jj in range(data.shape[0]):
    TE = data[jj,2]
    EK = 30     
    EK -= int(data[jj,3]/10)   # EK -= int(V/10)
    EK += (int(TE/4))
    if EK < 0:
        EK = 0 
    estimate[jj] = EK        

plt.figure()
plt.plot(data[:,3],data[:,10],'o',color='black')
plt.plot(data[:,3],estimate,'X',color='red')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Eis Kunden am Sonntag')
plt.show()



#%% Beste Eisstrategie als Funktion der Temperatur
Erwarteter_Gewinn = np.zeros([49,400])
Preisempfehlung =  np.zeros([49,])
for TE in range(-9,40):
    BestGewinn = 0
    for V in range(0,400):
      Erwarteter_Gewinn[TE+9,V] = (30 + int(TE/4) - int(V/10) )*(V-10)  # 10Pf ist der niedrigste mögliche Einkaufswert -> max Gewinn
      if (30 + int(TE/4) - int(V/10) ) < 0 :
          Erwarteter_Gewinn[TE+9,V] = 0 
      if Erwarteter_Gewinn[TE+9,V] > BestGewinn:
          BestGewinn =  Erwarteter_Gewinn[TE+9,V]
          Preisempfehlung[TE+9] = V
    

fig = plt.figure()
plt.imshow(Erwarteter_Gewinn.transpose()/1e2)
plt.plot(Preisempfehlung[0:41],color='white')
plt.plot([40,41,42,43,44,45,46,47,48],Preisempfehlung[40:],color='white')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.1)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.gca().invert_yaxis()
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Eis Strategie -Sonntag-')
cbar = plt.colorbar()
plt.clim(-5,30)
plt.text(55,410,'>=')
cbar.ax.set_ylabel('Erwarteter Gewinn (S=1) [DM]', rotation=90)
plt.savefig('OptimaleEisStrategie_So.jpg', dpi=600)
plt.show()


#%% Bratwurstkunde BK(T,V)
data = np.array(
[[1,	1,	33,	0,	0,	0,	0,	0,	20,    	0,	18,	0,	0,	0,	0,	0,	28,	0],
[1,	2,	34,	0,	0,	0,	0,	0,	40,	    0,	17,	0,	0,	0,	0,	0,	25,	0],
[1,	3,	18,	0,	0,	0,	0,	0,	60,    	0,	21,	0,	0,	0,	0,	0,	30,	0],
[1,	1,	23,	0,	0,	0,	0,	0,	80,	    0,	19,	0,	0,	0,	0,	0,	27,	0],
[1,	2,	15,	0,	0,	0,	0,	0,	100,	0,	20,	0,	0,	0,	0,	0,	30,	0],
[1,	3,	15,	0,	0,	0,	0,	0,	120,	0,	19,	0,	0,	0,	0,	0,	28,	0],
[1,	4,	17,	0,	0,	0,	0,	0,	140,	0,	18,	0,	0,	0,	0,	0,	28,	0],
[1,	5,	-6,	0,	0,	0,	0,	0,	160,	0,	24,	0,	0,	0,	0,	0,	34,	0],
[1,	1,	38,	0,	0,	0,	0,	0,	180,	0,	9,	0,	0,	0,	0,	0,	15,	0],
[1,	2,	33,	0,	0,	0,	0,	0,	200,	0,	9,	0,	0,	0,	0,	0,	16,	0],
[1,	3,	17,	0,	0,	0,	0,	0,	220,	0,	14,	0,	0,	0,	0,	0,	20,	0],
[1,	4,	1,	0,	0,	0,	0,	0,	240,	0,	18,	0,	0,	0,	0,	0,	31,	0],
[1,	5,	22,	0,	0,	0,	0,	0,	260,	0,	10,	0,	0,	0,	0,	0,	14,	0],
[1,	1,	35,	0,	0,	0,	0,	0,	280,	0,	5,	0,	0,	0,	0,	0,	8,	0],
[1,	2,	35,	0,	0,	0,	0,	0,	300,	0,	4,	0,	0,	0,	0,	0,	6,	0],
[1,	3,	35,	0,	0,	0,	0,	0,	320,	0,	3,	0,	0,	0,	0,	0,	5,	0],
[1,	4,	-9,	0,	0,	0,	0,	0,	340,	0,	16,	0,	0,	0,	0,	0,	23,	0],
[1,	5,	10,	0,	0,	0,	0,	0,	360,	0,	9,	0,	0,	0,	0,	0,	15,	0],
[1,	1,	27,	0,	0,	0,	0,	0,	380,	0,	2,	0,	0,	0,	0,	0,	2,	0],
[1,	2,	19,	0,	0,	0,	0,	0,	400,	0,	4,	0,	0,	0,	0,	0,	5,	0],
[1,	3,	17,	0,	0,	0,	0,	0,	420,	0,	4,	0,	0,	0,	0,	0,	5,	0],
[1,	4,	9,	0,	0,	0,	0,	0,	440,	0,	5,	0,	0,	0,	0,	0,	7,	0],
[1,	5,	12,	0,	0,	0,	0,	0,	440,	0,	3,	0,	0,	0,	0,	0,	6,	0],
[1,	1,	3,	0,	0,	0,	0,	0,	460,	0,	6,	0,	0,	0,	0,	0,	11,	0],
[1,	2,	-2,	0,	0,	0,	0,	0,	480,	0,	6,	0,	0,	0,	0,	0,	8,	0],
[1,	3,	27,	0,	0,	0,	0,	0,	500,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[1,	4,	30,	0,	0,	0,	0,	0,	500,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[1,	1,	-8,	0,	0,	0,	0,	0,	500,	0,	7,	0,	0,	0,	0,	0,	9,	0],
[1,	2,	22,	0,	0,	0,	0,	0,	500,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[1,	3,	-7,	0,	0,	0,	0,	0,	520,	0,	6,	0,	0,	0,	0,	0,	9,	0],
[1,	5,	7,	0,	0,	0,	0,	0,	540,	0,	1,	0,	0,	0,	0,	0,	2,	0],
[1,	3,	13,	0,	0,	0,	0,	0,	560,	0,	0,	0,	0,	0,	0,	0,	0,	0],
[1,	5,	-4,	0,	0,	0,	0,	0,	560,	0,	3,	0,	0,	0,	0,	0,	4,	0],
[1,	4,	-4,	0,	0,	0,	0,	0,	580,	0,	2,	0,	0,	0,	0,	0,	4,	0]]
)


estimate = np.zeros([data.shape[0],])
for jj in range(data.shape[0]):
    TE = data[jj,2]
    BK = 30     
    BK -= int(data[jj,8]/20)   # EK -= int(V/10)
    BK -= int(TE/3)
    if BK < 0:
        BK = 0 
    estimate[jj] = BK
        

plt.figure()
plt.plot(data[:,8],data[:,10],'o',color='black')
plt.plot(data[:,8],estimate,'X',color='red')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Bratwurst Kunden am Wochentag')
plt.show()

#%% Beste Bratwurstsrategie als Funktion der Temperatur
Erwarteter_Gewinn = np.zeros([49,600])
Preisempfehlung =  np.zeros([49,])
for TE in range(-9,40):
    BestGewinn = 0
    for V in range(0,600):
      Erwarteter_Gewinn[TE+9,V] = (30- int(TE/3.) - int(V/20) )*(V-50)  # 50 ist der niedrigste Einkaufswert -> max Gewinn
      if (30- int(TE/3.) - int(V/20) ) < 0 :
          Erwarteter_Gewinn[TE+9,V] = 0 
      if Erwarteter_Gewinn[TE+9,V] > BestGewinn:
          BestGewinn =  Erwarteter_Gewinn[TE+9,V]
          Preisempfehlung[TE+9] = V
    

fig = plt.figure()
plt.imshow(Erwarteter_Gewinn.transpose()/1e2)
plt.plot(Preisempfehlung[0:42],color='white')
plt.plot([41,42,43,44,45,46,47,48],Preisempfehlung[41:],color='white')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.05)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.gca().invert_yaxis()
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Bratwurst Strategie -Wochentag-')
cbar = plt.colorbar()
plt.clim([-10,80])
cbar.ax.set_ylabel('Erwarteter Gewinn (S=1) [DM]', rotation=90)
plt.savefig('OptimaleBratwurstStrategie.jpg', dpi=600)
plt.show()


#%% Bratwurst BK(T) SAMSTAG

data = np.array([
[1,	6,	9,	0,	0,	0,	0,	0,	200,	0,	27,	0,	0,	0,	0,	0,	46,	0,	0,	46],
[1,	6,	37,	0,	0,	0,	0,	0,	150,	0,	21,	0,	0,	0,	0,	0,	33,	0,	0,	33],
[1,	6,	19,	0,	0,	0,	0,	0,	240,	0,	22,	0,	0,	0,	0,	0,	34,	0,	0,	34],
[1,	6,	27,	0,	0,	0,	0,	0,	100,	0,	26,	0,	0,	0,	0,	0,	36,	0,	0,	36],
[1,	6,	1,	0,	0,	0,	0,	0,	300,	0,	25,	0,	0,	0,	0,	0,	36,	0,	0,	36],
[1,	6,	19,	0,	0,	0,	0,	0,	600,	0,	4,	0,	0,	0,	0,	0,	7,	0,	0,	7],
[2,	6,	-9,	0,	0,	0,	0,	0,	500,	0,	18,	0,	0,	0,	0,	0,	27,	0,	0,	27],
[2,	6,	0,	0,	0,	0,	0,	0,	700,	0,	5,	0,	0,	0,	0,	0,	9,	0,	0,	9]])

estimate = np.zeros([data.shape[0],])
for jj in range(data.shape[0]):
    TE = data[jj,2]
    BK = 40     
    BK -= int(data[jj,8]/20)   # EK -= int(V/10)
    BK -= int(TE/3)
    if BK < 0:
        BK = 0 
    estimate[jj] = BK
        

plt.figure()
plt.plot(data[:,2],data[:,10],'o',color='black')
plt.plot(data[:,2],estimate,'X',color='red')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Bratwurst Kunden am Samstag')
plt.show()

Erwarteter_Gewinn = np.zeros([49,600])
Preisempfehlung =  np.zeros([49,])
for TE in range(-9,40):
    BestGewinn = 0
    for V in range(0,600):
      Erwarteter_Gewinn[TE+9,V] = (40- int(TE/3.) - int(V/20) )*(V-50)  # 50 ist der niedrigste Einkaufswert -> max Gewinn
      if (40- int(TE/3.) - int(V/20) ) < 0 :
          Erwarteter_Gewinn[TE+9,V] = 0 
      if Erwarteter_Gewinn[TE+9,V] > BestGewinn:
          BestGewinn =  Erwarteter_Gewinn[TE+9,V]
          Preisempfehlung[TE+9] = V
    

fig = plt.figure()
plt.imshow(Erwarteter_Gewinn.transpose()/1e2)
plt.plot(Preisempfehlung[0:42],color='white')
plt.plot([41,42,43,44,45,46,47,48],Preisempfehlung[41:],color='white')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.05)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.gca().invert_yaxis()
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.text(55,660,'>=')
plt.title('Optimale Bratwurst Strategie -Wochenende-')
cbar = plt.colorbar()
plt.clim([-10,80])
cbar.ax.set_ylabel('Erwarteter Gewinn (S=1) [DM]', rotation=90)
plt.savefig('OptimaleBratwurstStrategie_WE.jpg', dpi=600)
plt.show()




#%% Bratwurst BK(T) SONNTAG
data = np.array([
[2,	7,	23,	0,	0,	0,	0,	0,	100,	0,	28,	0,	0,	0,	0,	0,	40,	0,	0,	40],
[2,	7,	-3,	0,	0,	0,	0,	0,	300,	0,	26,	0,	0,	0,	0,	0,	41,	0,	0,	41],
[2,	7,	34,	0,	0,	0,	0,	0,	150,	0,	22,	0,	0,	0,	0,	0,	35,	0,	0,	35],
[2,	7,	15,	0,	0,	0,	0,	0,	250,	0,	23,	0,	0,	0,	0,	0,	34,	0,	0,	34],
[2,	7,	20,	0,	0,	0,	0,	0,	400,	0,	14,	0,	0,	0,	0,	0,	19,	0,	0,	19],
[1,	7,	-2,	0,	0,	0,	0,	0,	500,	0,	15,	0,	0,	0,	0,	0,	23,	0,	0,	23],
[1,	7,	9,	0,	0,	0,	0,	0,	430,	0,	16,	0,	0,	0,	0,	0,	21,	0,	0,	21]])


estimate = np.zeros([data.shape[0],])
for jj in range(data.shape[0]):
    TE = data[jj,2]
    BK = 40     
    BK -= int(data[jj,8]/20)   # EK -= int(V/10)
    BK -= int(TE/3)
    if BK < 0:
        BK = 0 
    estimate[jj] = BK
        

plt.figure()
plt.plot(data[:,2],data[:,10],'o',color='black')
plt.plot(data[:,2],estimate,'X',color='red')
plt.xlabel('Preis [pf]')
plt.ylabel('Kunden #')
plt.title('Bratwurst Kunden am Sonntag')
plt.show()




#%% EK(T)
data = np.array(
[[1,1,	18,	0,	0,	0,	0,	0,	0,	0,	24,	38,	0,	0,	0,	0,	0,	0,	38,	0],
[1,	2,	25,	0,	0,	0,	0,	0,	0,	0,	26,	35,	0,	0,	0,	0,	0,	0,	35,	0],
[1,	3,	29,	0,	0,	0,	0,	0,	0,	0,	27,	38,	0,	0,	0,	0,	0,	0,	38,	0],
[1,	4,	9,	0,	0,	0,	0,	0,	0,	0,	22,	31,	0,	0,	0,	0,	0,	0,	31,	0],
[1,	5,	11,	0,	0,	0,	0,	0,	0,	0,	22,	32,	0,	0,	0,	0,	0,	0,	32,	0],
[1,	1,	8,	0,	0,	0,	0,	0,	0,	0,	22,	34,	0,	0,	0,	0,	0,	0,	34,	0],
[1,	2,	0,	0,	0,	0,	0,	0,	0,	0,	20,	32,	0,	0,	0,	0,	0,	0,	32,	0],
[1,	3,	-1,	0,	0,	0,	0,	0,	0,	0,	20,	35,	0,	0,	0,	0,	0,	0,	35,	0],
[1,	4,	15,	0,	0,	0,	0,	0,	0,	0,	23,	39,	0,	0,	0,	0,	0,	0,	39,	0],
[1,	5,	-6,	0,	0,	0,	0,	0,	0,	0,	19,	32,	0,	0,	0,	0,	0,	0,	32,	0],
[1,	1,	36,	0,	0,	0,	0,	0,	0,	0,	29,	36,	0,	0,	0,	0,	0,	0,	36,	0],
[1,	2,	32,	0,	0,	0,	0,	0,	0,	0,	28,	41,	0,	0,	0,	0,	0,	0,	41,	0],
[1,	3,	-1,	0,	0,	0,	0,	0,	0,	0,	20,	30,	0,	0,	0,	0,	0,	0,	30,	0],
[1,	4,	-9,	0,	0,	0,	0,	0,	0,	0,	18,	30,	0,	0,	0,	0,	0,	0,	30,	0]])


estimate_E = np.zeros([49,])
temp = np.zeros([49,])
jj = 0 
for TE in range(-9,40):    
    EK = 20 + int(TE/4)
    estimate_E[jj] = EK
    temp[jj] = TE
    jj+=1
        

plt.figure()
#plt.plot(data[:,2],data[:,3],'X',color='black')
#plt.plot(temp,estimate,'--',color='black')
plt.plot(data[:,2],data[:,10],'X',color='red')
plt.plot(temp,estimate_E,'--',color='red')

plt.show()



#%%
#### WERKTAG
data = np.array(
[[1,	1,	5,							60,	13,	8,	1,	13,	11,	15,	32,	35,	47],
[1,	1,	1,								60,	7,	5,	6,	8,	15,	18,	28,	26,	46],
[1,	2,	2,								60,	11,	8,	11,	1,	15,	27,	20,	31,	47],
[1,	1,	5,								60,	8,	11,	4,	5,	18,	25,	21,	28,	46],
[1,	1,	-1,								60,	10,	4,	4,	8,	16,	18,	25,	26,	43],
[1,	1,	5,								60,	10,	5,	7,	8,	14,	24,	19,	30,	43],
[1,	1,	9,								59,	5,	6,	12,	10,	14,	13,	21,	33,	34],
[1,	1,	21,								58,	9,	8,	8,	9,	17,	17,	18,	34,	35],
[1,	1,	32,								58,	11,	5,	17,	13,	13,	20,	13,	46,	33],
[1,	1,	9,								59,	8,	6,	15,	4,	15,	24,	20,	33,	44],
[1,	1,	25,								58,	8,	14,	15,	3,	13,	17,	12,	40,	29],
[1,	1,	5,								60,	6,	8,	10,	6,	16,	19,	23,	30,	42],
[1,	1,	33,								57,	14,	6,	10,	13,	16,	19,	11,	43,	30],
[1,	1,	-9,								61,	6,	5,	6,	8,	16,	24,	25,	25,	49],
[1,	1,	-2,								60,	6,	8,	7,	9,	16,	25,	22,	30,	47],
[1,	1,	-7,								61,	5,	8,	9,	6,	15,	25,	25,	28,	50],
[1,	1,	26,								58,	15,	4,	6,	14,	17,	13,	20,	39,	33],
[1,	1,	37,								57,	14,	9,	7,	14,	16,	21,	8,	44,	29],
[1,	1,	23,								58,	10,	5,	6,	19,	14,	17,	18,	40,	35],
[1,	1,	25,								58,	7,	9,	5,	20,	15,	13,	24,	41,	37],
[2,	2,	4,								60,	5,	9,	8,	11,	14,	16,	27,	33,	43],
[1,	1,	36,								57,	12,	10,	20,	5,	15,	13,	15,	47,	28],
[1,	1,	-9,								61,	1,	4,	15,	5,	15,	25,	24,	25,	49],
[1,	1,	2,								60,	12,	8,	5,	5,	16,	15,	35,	30,	50],
[1,	1,	15,								58,	8,	10,	10,	7,	13,	16,	25,	35,	41],
[1,	1,	13,								59,	11,	7,	6,	9,	16,	16,	20,	33,	36],
[1,	1,	25,								58,	19,	7,	5,	6,	13,	20,	16,	37,	36],
[1,	1,	33,								57,	7,	9,	22,	7,	17,	12,	17,	45,	29],
[1,	1,	20,								59,	13,	13,	8,	6,	14,	16,	20,	40,	36],
[1,	1,	5,								60,	6,	5,	15,	6,	13,	25,	18,	32,	43],
[1,	1,	17,								59,	6,	11,	12,	10,	13,	14,	19,	39,	33],
[1,	1,	14,								59,	6,	8,	13,	7,	13,	12,	23,	34,	35],
[1,	1,	22,								58,	6,	12,	12,	7,	17,	17,	18,	37,	35],
[1,	1,	39,								56,	17,	8,	5,	14,	15,	13,	11,	44,	24],
[1,	1,	11,								59,	12,	2,	14,	2,	18,	18,	24,	30,	42],
[1,	1,	3,								59,	8,	1,	11,	7,	15,	23,	19,	27,	42],
[1,	1,	30,								57,	12,	11,	10,	6,	15,	13,	15,	39,	28]])


estimate = np.zeros([49,])
estimate_E = np.zeros([49,])
estimate_B = np.zeros([49,])
estimate_Z = np.zeros([49,])
temp = np.zeros([49,])
jj = 0 
for TE in range(-9,40):    
    EK = 20 + int(TE/3.5)
    BK = 30 - int(TE/3)
    ZK = 10 
    AK = ZK+BK+EK 
    estimate[jj] = AK
    estimate_E[jj] = EK
    estimate_B[jj] = BK
    estimate_Z[jj] = ZK
    temp[jj] = TE
    jj+=1
        


plt.figure()
plt.plot(data[:,2],data[:,3],'X',color='black')
plt.plot(temp,estimate,'--',color='black')
plt.plot(data[:,2],data[:,11]*0.7,'X',color='red')
plt.plot(temp,estimate_E,'--',color='red')
plt.plot(data[:,2],data[:,12]*0.7,'X',color='cyan')
plt.plot(temp,estimate_B,'--',color='cyan')
plt.plot(data[:,2],data[:,8]*0.7,'X',color='magenta')
plt.plot(temp,estimate_Z,'--',color='magenta')

plt.show()


#%%

#### SAMSTAGS

data = np.array(
[[1,	6,	17,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	76,	18,	13,	12,	7,	17,	24,	27,	50,	51],
[1,	6,	10,	0.01,	0,		0,	     0,   0.01	,	0.01,	0.0 ,   76,	3,	33,	5,	0,	16,	48,	2,	41,	50],
[1,	6,	0,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	77,	12,	7,	9,	8,	16,	31,	28,	36,	59],
[1,	6,	-5,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	77,	9,	9,	15,	3,	14,	32,	29,	36,	61],
[1,	6,	7,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	76,	7,	10,	13,	5,	15,	28,	30,	35,	58],
[1,	6,	9,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	76,	8,	7,	13,	11,	17,	31,	23,	39,	54],
[1,	6,	23,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	75,	13,	9,	9,	13,	20,	31,	14,	44,	45],
[1,	6,	1,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	77,	17,	9,	5,	7,	19,	23,	34,	38,	57],
[1,	6,	37,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	74,	17,	14,	11,	11,	17,	23,	18,	53,	41],
[1,	6,	27,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	74,	7,	6,	11,	21,	18,	21,	24,	45,	45]])


estimate = np.zeros([49,])
estimate_E = np.zeros([49,])
estimate_B = np.zeros([49,])
estimate_Z = np.zeros([49,])
temp = np.zeros([49,])
jj = 0 
for TE in range(-9,40):    
    EK = 25 + int(TE/4)
    BK = 40 - int(TE/3)
    ZK = 12 
    AK = ZK+BK+EK 
    estimate[jj] = AK
    estimate_E[jj] = EK
    estimate_B[jj] = BK
    estimate_Z[jj] = ZK
    temp[jj] = TE
    jj+=1
        


plt.figure()
plt.plot(data[:,2],data[:,10],'X',color='black')
plt.plot(temp,estimate,'--',color='black')
plt.plot(data[:,2],data[:,18]*0.7,'X',color='red')
plt.plot(temp,estimate_E,'--',color='red')
plt.plot(data[:,2],data[:,19]*0.7,'X',color='cyan')
plt.plot(temp,estimate_B,'--',color='cyan')
plt.plot(data[:,2],data[:,15]*0.7,'X',color='magenta')
plt.plot(temp,estimate_Z,'--',color='magenta')

plt.show()



#%%
#### SONNTAGS 


data = np.array(
[[1,	7,	20,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	16,	13,	8,	11,	25,	29,	23,	48,	52],
[1,	7,	37,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	82,	16,	17,	15,	9,	20,	21,	20,	57,	41],
[1,	7,	17,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	14,	7,	11,	23,	22,	24,	26,	55,	50],
[2,	7,	12,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	17,	12,	8,	13,	18,	31,	29,	50,	60],
[1,	7,	10,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	13,	8,	18,	10,	21,	25,	30,	49,	55],
[1,	7,	2,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	85,	7,	18,	6,	15,	21,	23,	29,	46,	52],
[1,	7,	0,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	85,	15,	13,	10,	4,	22,	39,	20,	42,	59],
[1,	7,	6,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	19,	7,	7,	15,	24,	26,	27,	48,	53],
[1,	7,	10,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	83,	10,	10,	20,	8,	25,	26,	29,	48,	55],
[1,	7,	17,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	9,	15,	19,	5,	26,	30,	24,	48,	54],
[1,	7,	26,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	83,	11,	9,	20,	9,	22,	33,	13,	49,	46],
[1,	7,	36,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	82,	17,	10,	17,	20,	24,	28,	20,	64,	48],
[1,	7,	7,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	0.01,	84,	14,	12,	11,	8,	23,	28,	26,	45,	54]])



estimate = np.zeros([49,])
estimate_E = np.zeros([49,])
estimate_B = np.zeros([49,])
estimate_Z = np.zeros([49,])
temp = np.zeros([49,])
jj = 0 
for TE in range(-9,40):    
    EK = 30 + int(TE/4)
    BK = 40 - int(TE/3)
    ZK = 15 
    AK = ZK+BK+EK 
    estimate[jj] = AK
    estimate_E[jj] = EK
    estimate_B[jj] = BK
    estimate_Z[jj] = ZK
    temp[jj] = TE
    jj+=1
        


plt.figure()
plt.plot(data[:,2],data[:,10],'X',color='black')
plt.plot(temp,estimate,'--',color='black')
plt.plot(data[:,2],data[:,18]*0.7,'X',color='red')
plt.plot(temp,estimate_E,'--',color='red')
plt.plot(data[:,2],data[:,19]*0.7,'X',color='cyan')
plt.plot(temp,estimate_B,'--',color='cyan')
plt.plot(data[:,2],data[:,15]*0.7,'X',color='magenta')
plt.plot(temp,estimate_Z,'--',color='magenta')

plt.show()