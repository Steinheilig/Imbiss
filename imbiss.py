# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 21:41:02 - 00:10:00 2021   ;) 
@author: Steinheilig

Dieses Program ist eine 1:1 Implementation (der Spielmechanik) von 
"Imbiss-Bude" von F. Brall 1983 für Apple II, Homecomputer 8/1983, S. 37-41
"Imbiss" von O.Schwald 1984 für Commodore C64, Homecomputer 10/1984, S. 55-58 

Exploits der Spielmechanik für diese Spielversion:
1) 10% der Fälle, keine Prüfung von Eispreis => Ein Eis super billig -> EK  (nur abhängig von kleinstem Eispreis (1440))  // Anderen Eissorten Max preis wird bezahllt
2) 10% der Fälle, keine Prüfung von Bratwurst-/Pommespreis=> Eins super billig -> BK  (nur abhängig von kleinstem Preis (1440))  // Andere Max preis wird bezahllt
3) Kein Einfluss des Cola Preises auf Kunden (Cola Kunden sind zufällige Eiskunden) / keine Prüfung von Colapreis => Jeder Cola Preis wird bezahlt in ca. für EK/4 % Der Fälle

Spielgeschichte: 
F. Brall    1983,   Apple II,   "Imbiss-Bude"
O. Schwald  1984,   C64,        "Imbiss"
T. Bauer    1984,   VZ200,      "Imbiss"        *nicht veröffentlicht*
T. Bauer    1986,   CPC664,     "Imbiss"        *nicht veröffentlicht*
O. Schwald  1987,   Amiga,      "Imbiss III"
T. Bauer    1991,   PC,         "Imbiss"
A. Kern     1994,   Amiga,      "Tom's Imbiss"
A. Kern     2009,   PC,         "Tom's Imbiss"
A. Kern     2011,   Crossplat*  "Tom's Imbiss"
L. Brämer   2019,   Amiga,      "Tom's Imbiss"
T. Bauer    2021,   Android,    "Imbiss Classic"
Steinheilig 2021,   PC,         "Imbiss"
  
*Crossplatform:  AmigaOS 3 (m68k) AmigaOS 4 (ppc) Android (arm) AROS (x86)
iOS (arm) Linux (x86) Linux (x64)
Linux (arm) Linux (ppc) macOS (x86) macOS (x64) macOS (ppc)
MorphOS (ppc) WarpOS (m68k/ppc) Windows (x86) Windows (x64)
    
"""

import numpy as np 


# init 
T = 0                          # Tage
Wo = 0                         # Woche
Tage = ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sontag']
Waren = ['Schokoeis','Vanilleeis','Erdbeereis','Cola','Zigaretten','Bratwurst','Pommes']
K = 1000                       # Kontostand (in Pf)
TE = np.random.randint(-9,40)  # Temperatur
H = np.zeros([7,])             # Einkaufspreise
V = np.zeros([7,])             # Verkaufspreise
W = np.zeros([7,],dtype=int)   # Warenbestand

# test Simulation 
#W = W+10 
#V = [99,99,99,499,799,230,240]


def plot_intro():
    print('')
    print('     IIIIIII     MM        M     BBbBB      IIIIIIIII      SSSSSS    SSSSSS')
    print('       III       MMm      mM     BB  BB        III        SSS       SSS ')
    print('       III       MM m    m M     BB   bB       III        sSS       sSS')
    print('       III       MM  m  m  M     BBbBB         III          ssSs      sSs')
    print('       III       MM   mMm  M     BB  BB        III            sSS      sSS')
    print('       III       MM    m   M     BB   bB       III            SSs      SSs')
    print('       III       MM        M     BB  bB        III            sSS      sSS')
    print('     IIIIIII     MM        M     BBbBB      IIIIIIIII     SSSSss    SSSSss')
    print('')
    print('  by Steinheilig (2021)')
    

def plot_inventar():
    print('')
    print('Woche',Wo,Tage[T],'Temperatur:',TE,'°C',' Kontostand',K/100.,'DM')
    print('########################################')
    print('Ware\t\t Anzahl\tVerkaufspreis',)
    print('########################################')
    for Ware in range(7):
       if Ware == 3 or Ware == 6:
           print(Waren[Ware],'\t\t',W[Ware],'\t',V[Ware])         
       else:
         print(Waren[Ware],'\t',W[Ware],'\t',V[Ware])         
    print('########################################')


def Einkaufspreise(H):
  Z1=10;Z2=40
  if TE > 5:
     Z1=20;Z2=45    
  if TE > 10:
     Z1=30;Z2=50    
  if TE > 15:
     Z1=40;Z2=60    
  if TE > 20:
     Z1=40;Z2=70    
  if TE > 30:
     Z1=50;Z2=90    
  if TE > 35:
     Z1=80;Z2=100      
  if T == 5:  # Freitags Malus für Eis, dafür wird die Bratwurst billiger... 
     Z1 +=15
     Z2 +=15
  H = [np.random.randint(Z1,Z2),np.random.randint(Z1,Z2),np.random.randint(Z1,Z2),
       np.random.randint(Z1,Z2)+10,
       np.random.randint(4,9)*50,
       150-np.random.randint(Z1,Z2),
       170-np.random.randint(Z1,Z2),
       ]
  return H 

    
def Einkaufen(WS,AS,K):
    print('Einkaufen von ',Waren[WS],'X',AS,'zu je',H[WS],' ')
    if K - H[WS]*AS > 0:
        K -= H[WS]*AS
        W[WS] += AS
    else:
        print('nicht genügend Geld in der Tasche')
    return K


def Kaufen(WS,S,K):
    print('Kunde: Könnten Sie mir bitte',S,Waren[WS],'geben')
    if W[WS] == 0:
        print(Waren[WS],'- nix mehr zu verkaufen')
        return K
    if W[WS] <= S:
        print('Das waren die letzten',Waren[WS])    
    if S > W[WS]:
      W[WS] = 0 
      K += V[WS]
    else:
      W[WS] -= S
      K += S*V[WS]
    return K
    

def Kunden_Simulation(K):
    EK = 10  # Eis Kunden
    ZK = 10  # Zigaretten Kunden 
    BK = 30  # Bratwurst Kunden 
    if T == 6:  # Samstag
       EK = 15
       ZK = 13
       BK = 40
    if T == 7:  # Sontag
       EK = 20
       ZK = 18
       BK = 40
    
    # Berechnen der Kunden als Funktion des Preise 
    EK -= int(np.min(V[0:2])/10)
    ZK -= int(V[4]/100)
    BK -= int(np.min(V[5:6])/20)
    
    # Temperatur Korrektur
    EK += abs(int(TE/2))
    BK -= abs(int(TE/2))
    
    AK = ZK+BK+EK
    print('Kunden gesamt:\t\t',AK)
    print('Eis Kunden:\t\t',EK)
    print('Zigaret. Kunden:\t',ZK)
    print('Bratwurst Kunden:\t',BK)
    if AK < 0:
        AK = 0 
        
    if AK < 2:
        return K
    
    for Kunde in range(AK):
        #print('Kunde',Kunde)
        kauf = False
        E = np.random.randint(0,9)    # eine Zufallsvariabe für Anzahl Einheiten zu kaufen und Preise ignorieren 
        if E == 2:
            S = 2
        else: 
            S = 1 
            
        while not(kauf):
            # eine zufällige Ware wählen 
            Z = np.random.randint(0,7)
            
            if Z < 4 and  EK == 0:  # keine Eiskunden mehr  
                #print('keine Eiskunden mehr')
                kauf = False  
                continue
            
            if Z == 4 and  ZK == 0:  # keine Zigarettenkunden mehr  
                continue

            if Z > 4 and  BK == 0:  # keine Bratwurstkunden mehr  
                continue

            if Z == 0: # Schokoeis
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[0]-V[1] > 20:
                       K = Kaufen(1,S,K)
                       EK -= 1; kauf = True  
                       break
                   if V[0]-V[2] > 20:
                       K = Kaufen(2,S,K)
                       EK -= 1; kauf = True  
                       break 
                K = Kaufen(0,S,K)  
                EK -= 1; kauf = True  
                   
            if Z == 1: # Vanilleeis
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[1]-V[0] > 20:
                       K = Kaufen(0,S,K)
                       EK -= 1; kauf = True  
                       break 
                   if V[1]-V[2] > 20:
                       K = Kaufen(2,S,K)
                       EK -= 1; kauf = True  
                       break
                K = Kaufen(1,S,K)  
                EK -= 1; kauf = True  
        
            if Z == 2: # Erdbeereis
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[2]-V[0] > 20:
                       K = K = Kaufen(0,S,K)
                       EK -= 1; kauf = True  
                       break 
                   if V[2]-V[1] > 20:
                       K = Kaufen(1,S,K)
                       EK -= 1; kauf = True  
                       break 
                K = Kaufen(2,S,K)  
                EK -= 1; kauf = True     
                
            if Z == 3: # Cola    ## KEINE PREISPRÜFUNG COLA!!!
                K = Kaufen(3,S,K)  
                EK -= 1; kauf = True             
            
            if Z == 4: # Zigarette   ## PREISPRÜFUNG indirekt über ZK 
                K = Kaufen(4,S,K)  
                ZK -= 1; kauf = True                            
                
            if Z == 5: # Bratwurst
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[5]-V[6] > 30:
                       K = Kaufen(6,S,K)
                       BK -= 1; kauf = True  
                       break
                K = Kaufen(5,S,K)  
                BK -= 1; kauf = True  
        
            if Z == 6: # Pommes
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[6]-V[5] > 30:
                       K = Kaufen(5,S,K)
                       BK -= 1; kauf = True  
                       break
                K = Kaufen(6,S,K)  
                BK -= 1; kauf = True      
            
    return K


### Spiel einmal für zwei Wochen starten 
plot_intro()
for day in range(14):  # zwei Wochen fix ;) 
    TE = np.random.randint(-9,40)  # Temperatur
    H = Einkaufspreise(H)

    plot_inventar()
    jn = input('Möchten Sie Einkaufen: (j/n/c) ')
    if jn=='j':
        for Ware in range(7):
            ts = 'Wieviele '+Waren[Ware]+' zu je '+str(H[Ware])+'Pf? '
            AS = input(ts)       
            AS = int(AS)         
            K = Einkaufen(Ware,AS,K)
    if jn=='c':
        break
    plot_inventar()
    jn = input('Möchten Sie die Preise ändern: (j/n/c) ')
    if jn=='j':
        for Ware in range(7):
            ts = 'Preis für '+ Waren[Ware]+': '
            V[Ware] = input(ts)
    if jn=='c':
        break
    K = Kunden_Simulation(K)
    
    T += 1 
    if T > 6:
         T = 1
         Wo += 1

print('Ihr finaler Kontostand ist ',K/100.,'DM')
if K/(2*1e2) > 1000:
    print('Super gemacht')    
else:
    print('da geht noch was...')
