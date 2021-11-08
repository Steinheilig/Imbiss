# -*- coding: utf-8 -*-
"""

Machine Learning applied to defeat a 30 years old DOS game... 

Game mechanics 
"Imbiss" v. 5.4 by T. Bauer for IBM PC, Public Domain

Custom Environments in OpenAI’s Gym

Pocs (2020), Beginner’s Guide to Custom Environments in OpenAI’s Gym
How to set up, verify, and use a custom environment in reinforcement learning training with Python
https://towardsdatascience.com/beginners-guide-to-custom-environments-in-openai-s-gym-989371673952
https://github.com/MatePocs/gym-basic/blob/main/gym_basic/envs/basic_env_2.py

@author: Seinheilig, 2021
"""


import gym
import numpy as np 

class ImbissEnv(gym.Env):
    
        def __init__(self):
            self.action_space = gym.spaces.Box(np.array([0,0,0,0,0,0,0]),np.array([300,300,300,300,1300,1300,1300]),dtype=np.int16)  # price tags of all 7 elements
            self.observation_space = gym.spaces.Box(np.array([1,-9]),np.array([7,40])) # day of week / temperature
            
            #### ToDo: Observations better MultiDiscrete?  // requre different logic for TE... 
            ### self.observation_space = gym.spaces.MultiDiscrete([ 1, 49 ]) # day of week / temperature
            
        def rnd_state(self):
            #self.state = np.array([np.random.randint(1,7),np.random.randint(0,49)-9],dtype=np.int16) # full state (all days)
            self.state = np.array([1,np.random.randint(0,49)-9],dtype=np.int16) # only weekday...
            
        def step(self, action):
            '''
            single step
            return 
            '''
            V = action  # price tags (actions)
            T = self.state[0] # day of the week 
            TE = self.state[1] # temperatur
            K = 0 # money before selling 
            reward =  self.Customer_Simulation(V,T,TE,K,Version=3)                     
            self.rnd_state()
            done = True        
            info = {}       
            return self.state, reward, done, info
    
        def reset(self):
            self.rnd_state()
            return self.state
        
        def render(self, mode='human'):
            pass

        def Kaufen(self,WS,V,S,K):  
            """ reduced game mechanics for buying (DE: "kaufen")
            """
            debug_ = False 
            H = [10,10,10,20,200,35,55]  # lowest price possible 
            H = [10,10,10,20,200,50,70]  # good price..
            if debug_:
              Waren = ['Schokoeis','Vanilleeis','Erdbeereis','Cola','Zigaretten','Bratwurst','Pommes']
              print('Kunde: Könnten Sie mir bitte',S,Waren[WS],'geben')
              
            return K + S*V[WS] - S*H[WS]  # return new net balance after selling (income-expense)
        
        def Customer_Simulation(self,V,T,TE,K,Version=3):
            """ Spielmechanik - Kunden Simulation
        
            Args:
              V: Verkaufspreise
              T: Wochentag in [1:7]
              TE: Temperatur              
              K: Kontostand vor der Simulation
              Version: 1) "Imbiss-Bude" von F. Brall 1983 für Apple II
                       2) "Imbiss" von O. Schwald 1984 für Commodore C64
                       3) "Imbiss" von T. Bauer 1991 für PC
        
            Returns:
              K: Kontostand nach der Simulation
              
            """            
            debug_ = False
            if Version <3:
                EK = 10  # Eis Kunden
                ZK = 10  # Zigaretten Kunden 
                BK = 30  # Bratwurst Kunden 
                if T == 6:  # Samstag
                   EK = 15
                   ZK = 13
                   BK = 40
                if T == 7:  # Sonntag
                   EK = 20
                   ZK = 18
                   BK = 40
                
                # Korrektur der Kunden als Funktion des Preise 
                EK -= int(np.min(V[0:3])/10) # bugfix!!
                ZK -= int(V[4]/100)
                BK -= int(np.min(V[5:7])/20) # bugfix!!
                
                # Temperatur Korrektur
                EK += abs(int(TE/2))
                BK -= abs(int(TE/2))
            else:
                ##### "Imbiss" PC 1991 
                # 5 Änderungen zum Orginal:
                # 1) nutze max V der Warengruppe für Korrektur
                # 2) ZK = [10,12,15], ZK Basis Wochentag/Sa/So
                # 3) EK += 10 / andere Temperaturabhängigkeit
                # 4) BK andere Temperaturabhängigkeit        
                # 5) if ZK/EK/BK < 0 --> ZK/EK/BK = 0 bevor AK berechnet wird 
                EK = 20  # Eis Kunden 
                ZK = 10  # Zigaretten Kunden 
                BK = 30  # Bratwurst Kunden 
                if T == 6:  # Samstag
                   EK = 25
                   ZK = 12
                   BK = 40
                if T == 7:  # Sonntag
                   EK = 30
                   ZK = 15
                   BK = 40
                
                # Korrektur der Kunden als Funktion des Preise 
                EK -= int(np.max(V[0:4])/10)  # bugfix!!
                ZK -= int(V[4]/100)
                BK -= int(np.max(V[5:7])/20)  # bugfix!!
                
                # Temperatur Korrektur
                EK += abs(int(TE/4))
                BK -= abs(int(TE/3))
                
            # zu hoher Preis in einer Warengruppe (neg Kundenwert) führt nicht(!) zu einer Reduktion der Gesamtzahl der Kunden
            if BK < 0:
                BK = 0
            if ZK < 0:
                ZK = 0
            if EK < 0:
                EK = 0        
                
            AK = ZK+BK+EK  
            if debug_:
              print("Customer_Simulation:",V,T,TE,K)
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
                               K = self.Kaufen(1,V,S,K)
                               EK -= 1; kauf = True  
                               break
                           if V[0]-V[2] > 20:
                               K = self.Kaufen(2,V,S,K)
                               EK -= 1; kauf = True  
                               break 
                        K = self.Kaufen(0,V,S,K)  
                        EK -= 1; kauf = True  
                           
                    if Z == 1: # Vanilleeis
                        if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                           if V[1]-V[0] > 20:
                               K = self.Kaufen(0,V,S,K)
                               EK -= 1; kauf = True  
                               break 
                           if V[1]-V[2] > 20:
                               K = self.Kaufen(2,V,S,K)
                               EK -= 1; kauf = True  
                               break
                        K = self.Kaufen(1,V,S,K)  
                        EK -= 1; kauf = True  
                
                    if Z == 2: # Erdbeereis
                        if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                           if V[2]-V[0] > 20:
                               K = K = self.Kaufen(0,V,S,K)
                               EK -= 1; kauf = True  
                               break 
                           if V[2]-V[1] > 20:
                               K = self.Kaufen(1,V,S,K)
                               EK -= 1; kauf = True  
                               break 
                        K = self.Kaufen(2,V,S,K)  
                        EK -= 1; kauf = True     
                        
                    if Z == 3: # Cola    ## KEINE PREISPRÜFUNG COLA!!!
                        K = self.Kaufen(3,V,S,K)  
                        EK -= 1; kauf = True             
                    
                    if Z == 4: # Zigarette   ## PREISPRÜFUNG indirekt über ZK 
                        K = self.Kaufen(4,V,S,K)  
                        ZK -= 1; kauf = True                            
                        
                    if Z == 5: # Bratwurst
                        if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                           if V[5]-V[6] > 30:
                               K = self.Kaufen(6,V,S,K)
                               BK -= 1; kauf = True  
                               break
                        K = self.Kaufen(5,V,S,K)  
                        BK -= 1; kauf = True  
                
                    if Z == 6: # Pommes
                        if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                           if V[6]-V[5] > 30:
                               K = self.Kaufen(5,V,S,K)
                               BK -= 1; kauf = True  
                               break
                        K = self.Kaufen(6,V,S,K)  
                        BK -= 1; kauf = True      
                    
            return K
