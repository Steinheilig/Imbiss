# -*- coding: utf-8 -*-
"""

Machine Learning applied to defeat a 30 years old DOS game... 

Game mechanics 
"Imbiss" v. 5.4 by T. Bauer for IBM PC, 1991, Public Domain

Applying machine learning to find optimal sales prices, i.e. the sales prices optimizing the profit given the current temperature and day of the week. 
1) a) Using a machine learning model to approximate the profit as a function of sales prices, current temperature and day of the week.
   b) Employing an optimization strategie to find the optimal sales prices of the profit approximation function 
2) Employing reinforcement learning strategies to find optimal sales prices
3) DeepRL -> imbiss_RL_gym.py

ToDo:
    Quick& Dirty implementation ... Code refactoring badly needed...

@author: Steinheilig, 2021
"""

import numpy as np 
from sklearn.neural_network import MLPRegressor
#from sklearn.tree import DecisionTreeRegressor
#from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import pickle
#from scipy.optimize import minimize
import matplotlib.pyplot as plt #
from scipy import optimize
import time

#import os
#os.chdir('C:\EigeneLokaleDaten\Imbiss\git\Imbiss-main\Imbiss-main') # set current working dir if needed 

def DT_train(data):
    """ Train a ensemble of decision trees for model approximation of the profit as a function of current temperature and day of the week
    """
    X_train, X_test, y_train, y_test = train_test_split(data[:,0:10], data[:,10], random_state=1)
    clf = GradientBoostingRegressor(n_estimators=300,max_depth=10,random_state=1,verbose = 1).fit(X_train, y_train)
    #clf = AdaBoostRegressor(DecisionTreeRegressor(max_depth=10),
    #                       n_estimators=300, random_state=1).fit(X_train, y_train)
    clf.predict(X_test[:1])    
    print('Score on test set:',clf.score(X_test, y_test))
    return clf


def MLP_train(data):
    """ Train a multi layer perceptron (MLP) for model approximation of the profit as a function of current temperature and day of the week
    """
    # old (100, 50) = 5k
    # deeper (100,50,30,20,10) = 7.3k
    # shallow (50,25,10,5) = 1.55k
    # shallower (25,10,5,2) = 0.3k
    X_train, X_test, y_train, y_test = train_test_split(data[:,0:10], data[:,10], random_state=1)
    clf = MLPRegressor(hidden_layer_sizes=(25,10,5,2), activation='relu',  
                        random_state=1, max_iter=1000,
                        verbose=True).fit(X_train, y_train)
    clf.predict(X_test[:1])    
    print('Score on test set:',clf.score(X_test, y_test))
    return clf


def Kaufen(WS,V,S,K):  
    """ reduced game mechanics for customer buying (DE: "kaufen")
    """
    debug_ = False 
    H = [10,10,10,20,200,35,55]  # lowest price possible 
    H = [10,10,10,20,200,50,70]  # good price..
    if debug_:
      Waren = ['Schokoeis','Vanilleeis','Erdbeereis','Cola','Zigaretten','Bratwurst','Pommes']
      print('Kunde: Könnten Sie mir bitte',S,Waren[WS],'geben')      
    return K + S*V[WS] - S*H[WS]

def get_sample(OnlyWeekdays=True):
    """ generate a random sample, sales prices set randomly
    """
    debug_ = False
    K = 0          # money [Pf]
    Wo = 0                         # Week            
    TE = np.random.randint(-9,40)  # temperature [°C]
    if OnlyWeekdays:
      T = np.random.randint(0,4)  # day
    else:
      T = np.random.randint(0,6)  # day
    V = np.zeros([7,]) 
    V[0:4] = np.random.randint(0,299,[4,]) # price tags init and ice & coke
    V[4] = np.random.randint(0,1299) # price tag cigarettes
    V[5] = np.random.randint(0,1299) # price tag sausage
    V[6] = np.random.randint(0,1299) # price tag french frise
    K = Customer_Simulation(V,T,TE,K,Version=3)       
    sample = np.zeros([11,],dtype=int)    
    sample[0] = Wo
    sample[1] = T
    sample[2] = TE
    sample[3:10] = V
    sample[10] = K 
    if debug_:
        print(sample)
    return sample

def get_trainings_data(N,fname='data.npz',OnlyWeekdays=True):
    """ generate a training set of random sampless (sale prices set randomly)
    and store it in fname
    """
    print("Generate Trainings Data Set N=",N)
    data = np.zeros([N,11],dtype=int)
    for jj in range(N):
        data[jj,:] = get_sample(OnlyWeekdays)
    if fname != None:
        print('Trainings Data saved to',fname)
        np.savez(fname,data=data)
    return data

def load_trainings_data(fname='data.npz'):
    """ load a training data set
    """
    dataf = np.load(fname)
    data = dataf["data"]
    return data 

def MC_epsilon_greedy_naive(E=None,V=np.zeros([7,]),epsilon=0.5,Version=3):
    """ constant-alpha Monte Carlo method 
    with epsilon-greedy policy 
    naive tabular approach ;) 
    """
    if E == None:
        #E = np.zeros([49,299,299,299,299,1299,1299,1299], dtype=np.int8)  # expected reward
        E = np.zeros([49,29,29,29,29,129,129,129], dtype=np.uint8)  # expected reward (min=0 max=255 DM) 
    T = 0 # set day to monday / weekday
    K = 0 # balance before selling 
    alpha = 0.1
    TE = np.random.randomint(-9,40)    
    for jj in range (10000):
     if jj %10== 0:
      print("step",jj)
     for element in range(7):
        # estimate max
        idx = np.argmax(E[TE,element])
        if np.random.rand() > epsilon:
            V[element] = idx
        else:
            V[element] = np.random.randomint(E.shape()[element+1])
     K_new = Customer_Simulation(V,T,TE,K,Version=3)
     E[TE+9,:] = (1-alpha)*E[TE+9,:] + alpha*K_new
    return E      


def MC_epsilon_greedy(E=None,V=np.zeros([7,]),epsilon=0.5,Version=3):
  """ constant-alpha Monte Carlo method 
  with epsilon-greedy policy
  - dynamic value function table of top <max_mem> sale prices 
  """
  debug_ = False 
  max_mem = 100 
  if E == None:
        E = np.zeros([49,8,max_mem], dtype=np.int16)  # expected reward (min=0 max=255 DM) 
  T = 0 
  K = 0
  alpha = 0.4            
  for TE in range(-9,40):    
    for epoch in range (20000):
     #TE = np.random.randint(-9,40)
           
     if debug_:
       print("Temperatur",TE,"epoch",epoch,'returns',E[TE+9,7,:])      
     
     idx = np.argmax(E[TE+9,7,:]) # best result so far 
     if epoch %100== 0:
       print("Temperatur",TE,"epoch",epoch,'max_expected_return',E[TE+9,7,idx],'V',V)      
     if np.random.rand() > epsilon:
        # greedy 
        V = E[TE+9,0:7,idx]
     else:
        # random (in vincinity of the best result so far...)
        V = np.copy(E[TE+9,0:7,idx]) + np.random.randint(-25,25,[7,])            
        V[np.where(V<0)]=0
        # check if already in list 
        known = False
        for jj in range(max_mem):
          if np.all(E[TE+9,0:7,jj]==V) :
              idx = jj
              known = True
        if not(known):
          idx = np.argmin(E[TE+9,7,:])      
          K_new = Customer_Simulation(V,T,TE,K,Version=3)  
          if K_new > E[TE+9,7,idx]:
              E[TE+9,7,idx] = K_new
              E[TE+9,0:7,idx] = V                 
              
     K_new = Customer_Simulation(V,T,TE,K,Version=3)        
     # update expected reward
     E[TE+9,7,idx] = (1-alpha)*E[TE+9,7,idx] + alpha*K_new

  Preisempfehlung =  np.zeros([49,7])    
  for TE in range(-9,40):
      idx = np.argmax(E[TE+9,7,:]) # best result so far 
      print(TE,E[TE+9,0:7,idx])
      Preisempfehlung[TE+9,:] = E[TE+9,0:7,idx]      
  return E, Preisempfehlung



def MC_epsilon_greedy_quantized(E=None,V=None,epsilon=0.2,Version=3):
  """ constant-alpha Monte Carlo method 
  with epsilon-greedy policy
  - dynamic value function table of top <max_mem> sale prices 
  - quantization of sale prices 
  """
  debug_ = False 
  max_mem = 1000   
  T = 0 
  K = 0
  alpha = 0.2   

  epoch_k = 0 
  Kepochs = np.zeros([49*20000,])  

  if E == None:
        E = np.zeros([49,8,max_mem], dtype=np.int16)  # expected reward (min=0 max=255 DM) 
        for TE in range(-9,40):
          if type(V) is np.ndarray:
            E[TE+9,0:7,0] = V  # init with V0
            E[TE+9,7,0] = Customer_Simulation(V,T,TE,K,Version=3)  # init with max 
          for jj in range(1,max_mem):
            E[TE+9,0:7,jj] = np.random.randint(0,200,[7,])  # init with some random element values..   
    
  for TE in range(-9,40):    
    for epoch in range (20000):
     #TE = np.random.randint(-9,40)           
     if debug_:
       print("Temperatur",TE,"epoch",epoch,'returns',E[TE+9,7,0:5])      
     
     idx = np.argmax(E[TE+9,7,:]) # best result so far           
     Kepochs[epoch_k] = E[TE+9,7,idx]
     epoch_k += 1           
     if epoch %100== 0:
       print("Temperatur",TE,"epoch",epoch,'max_expected_return',E[TE+9,7,idx],'V',V)      
     if np.random.rand() > epsilon:
        # greedy 
        V = E[TE+9,0:7,idx]
     else:
        # random (in vincinity of the best result so far...)
        V = np.copy(E[TE+9,0:7,idx])
        
        element = np.random.randint(0,7)
        V[element] = E[TE+9,element,idx] + np.random.randint(-5,5)*5    
        element = np.random.randint(0,7)
        V[element] = E[TE+9,element,idx] + np.random.randint(-5,5)*5    
                
        #V = E[TE+9,0:7,idx] + np.random.randint(-25,25,[7,])            
        V[np.where(V<0)]=0
        # check if already in list 
        known = False
        
        if debug_:
          print(known,idx,V)
          time.sleep(1)
        
        for jj in range(max_mem):
          if np.all(E[TE+9,0:7,jj]==V):
              idx = jj
              known = True              
              if debug_:
                print("found:",E[TE+9,0:7,jj],V,jj)
              
        if not(known):
          idx = np.argmin(E[TE+9,7,:])      
          K_new = Customer_Simulation(V,T,TE,K,Version=3)  
          if K_new > E[TE+9,7,idx]:
              E[TE+9,7,idx] = K_new
              E[TE+9,0:7,idx] = V         
              
        if debug_:
          print(known,idx,V)
          time.sleep(1)
              
     K_new = Customer_Simulation(V,T,TE,K,Version=3)        
     # update expected reward
     E[TE+9,7,idx] = (1-alpha)*E[TE+9,7,idx] + alpha*K_new

  Preisempfehlung =  np.zeros([49,7])    
  for TE in range(-9,40):
      idx = np.argmax(E[TE+9,7,:]) # best result so far 
      print(TE,E[TE+9,0:7,idx])
      Preisempfehlung[TE+9,:] = E[TE+9,0:7,idx]
      
  return E, Preisempfehlung, Kepochs


def MC_epsilon_greedy_quantized_2ndVersion(E=None,V=None,epsilon=0.5,Version=3):
  """ constant-alpha Monte Carlo method 
  with epsilon-greedy policy
  - dynamic value function table of top <max_mem> sale prices 
  - quantization of sale prices 
  - different exploration behavior... 
  """    
  debug_ = False 
  max_mem = 200   
  max_epochs = 20000*2
  T = 0 
  K = 0
  alpha = 0.2   

  epoch_k = 0 
  Kepochs = np.zeros([49*max_epochs,])
  
  if E == None:
        E = np.zeros([49,8,max_mem], dtype=np.int16)  # expected reward (min=0 max=255 DM) 
        for TE in range(-9,40):
          if type(V) is np.ndarray:
            E[TE+9,0:7,0] = V  # init with V0
            E[TE+9,7,0] = Customer_Simulation(V,T,TE,K,Version=3)  # init with max 
          for jj in range(1,max_mem):
            E[TE+9,0:7,jj] = np.random.randint(0,200,[7,])  # init with some random element values..   
    
  for TE in range(-9,40):    
    for epoch in range (max_epochs):
     #TE = np.random.randint(-9,40)           
     if debug_:
       print("Temperatur",TE,"epoch",epoch,'returns',E[TE+9,7,0:5])      
     
     idx = np.argmax(E[TE+9,7,:]) # best result so far 
          
     Kepochs[epoch_k] = E[TE+9,7,idx]
     epoch_k += 1           
     if epoch %100== 0:
       print("Temperatur",TE,"epoch",epoch,'max_expected_return',E[TE+9,7,idx],'V',V)      
     if np.random.rand() > epsilon:
        # greedy 
        V = E[TE+9,0:7,idx]
     else:
        if  np.random.rand() > 0.5:
            idx = np.random.randint(0,max_mem)        
        else:
            
          # random (in vincinity of the best result so far...)
          V = np.copy(E[TE+9,0:7,idx])
        
          element = np.random.randint(0,7)
          V[element] = E[TE+9,element,idx] + np.random.randint(-5,5)*5    
          element = np.random.randint(0,7)
          V[element] = E[TE+9,element,idx] + np.random.randint(-5,5)*5    
                
          #V = E[TE+9,0:7,idx] + np.random.randint(-25,25,[7,])            
          V[np.where(V<0)]=0
          # check if already in list 
          known = False
        
          if debug_:
            print(known,idx,V)
            time.sleep(1)
        
          for jj in range(max_mem):
            if np.all(E[TE+9,0:7,jj]==V):
              idx = jj
              known = True              
              if debug_:
                print("found:",E[TE+9,0:7,jj],V,jj)
                
          if not(known):
            idx = np.argmin(E[TE+9,7,:])      
            K_new = Customer_Simulation(V,T,TE,K,Version=3)  
            if K_new > E[TE+9,7,idx]:
              E[TE+9,7,idx] = K_new
              E[TE+9,0:7,idx] = V         
              
          if debug_:
            print(known,idx,V)
            time.sleep(1)
              
     K_new = Customer_Simulation(V,T,TE,K,Version=3)        
     # update expected reward
     E[TE+9,7,idx] = (1-alpha)*E[TE+9,7,idx] + alpha*K_new

  Preisempfehlung =  np.zeros([49,7])    
  for TE in range(-9,40):
      idx = np.argmax(E[TE+9,7,:]) # best result so far 
      print(TE,E[TE+9,0:7,idx])
      Preisempfehlung[TE+9,:] = E[TE+9,0:7,idx]
      
  return E, Preisempfehlung, Kepochs


def Customer_Simulation(V,T,TE,K,Version=3):
    """ Game mechanics - customer simulation / Spielmechanik - Kunden Simulation 

    Args:
      K: Cash before / Kontostand vor der Simulation
      Version: 1) "Imbiss-Bude" von F. Brall 1983 für Apple II
               2) "Imbiss" von O. Schwald 1984 für Commodore C64
               3) "Imbiss" von T. Bauer 1991 für PC

    Returns:
      K: Cash after / Kontostand nach der Simulation      
    """
    debug_ = False
    if Version <3:
        EK = 10  # ice customer / Eis Kunden
        ZK = 10  # cigarettes customer / Zigaretten Kunden 
        BK = 30  # Bratwurst Kunden 
        if T == 6:  # saturday / Samstag
           EK = 15
           ZK = 13
           BK = 40
        if T == 7:  # sunday / Sonntag
           EK = 20
           ZK = 18
           BK = 40
        
        # correct customer number as function of sales prices / Korrektur der Kunden als Funktion des Preise 
        EK -= int(np.min(V[0:3])/10) # bugfix!!
        ZK -= int(V[4]/100)
        BK -= int(np.min(V[5:7])/20) # bugfix!!
        
        # temperature correction/  Temperatur Korrektur
        EK += int(TE/2)
        BK -= int(TE/2)
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
        EK += int(TE/4)
        BK -= int(TE/3)
        
    # zu hoher Preis in einer Warengruppe (neg Kundenwert) führt nicht(!) zu einer Reduktion der Gesamtzahl der Kunden
    if BK < 0:
        BK = 0
    if ZK < 0:
        ZK = 0
    if EK < 0:
        EK = 0        
        
    AK = ZK+BK+EK  
    if debug_:
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
                       K = Kaufen(1,V,S,K)
                       EK -= 1; kauf = True  
                       break
                   if V[0]-V[2] > 20:
                       K = Kaufen(2,V,S,K)
                       EK -= 1; kauf = True  
                       break 
                K = Kaufen(0,V,S,K)  
                EK -= 1; kauf = True  
                   
            if Z == 1: # Vanilleeis
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[1]-V[0] > 20:
                       K = Kaufen(0,V,S,K)
                       EK -= 1; kauf = True  
                       break 
                   if V[1]-V[2] > 20:
                       K = Kaufen(2,V,S,K)
                       EK -= 1; kauf = True  
                       break
                K = Kaufen(1,V,S,K)  
                EK -= 1; kauf = True  
        
            if Z == 2: # Erdbeereis
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[2]-V[0] > 20:
                       K = K = Kaufen(0,V,S,K)
                       EK -= 1; kauf = True  
                       break 
                   if V[2]-V[1] > 20:
                       K = Kaufen(1,V,S,K)
                       EK -= 1; kauf = True  
                       break 
                K = Kaufen(2,V,S,K)  
                EK -= 1; kauf = True     
                
            if Z == 3: # Cola    ## KEINE PREISPRÜFUNG COLA!!!
                K = Kaufen(3,V,S,K)  
                EK -= 1; kauf = True             
            
            if Z == 4: # Zigarette   ## PREISPRÜFUNG indirekt über ZK 
                K = Kaufen(4,V,S,K)  
                ZK -= 1; kauf = True                            
                
            if Z == 5: # Bratwurst
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[5]-V[6] > 30:
                       K = Kaufen(6,V,S,K)
                       BK -= 1; kauf = True  
                       break
                K = Kaufen(5,V,S,K)  
                BK -= 1; kauf = True  
        
            if Z == 6: # Pommes
                if E != 3:  # Preisprüfung überspringen? (in 10% der Fälle)
                   if V[6]-V[5] > 30:
                       K = Kaufen(5,V,S,K)
                       BK -= 1; kauf = True  
                       break
                K = Kaufen(6,V,S,K)  
                BK -= 1; kauf = True                  
    return K



#%%
# =============================================================================
# 1) a) Using a machine learning model to approximate the profit as a function 
#       of current temperature, day of the week & sales prices (f(TE,T,V).
#    b) Employing an optimization strategie to find the optimal sale prices 
#       of the profit approximation function. 
# =============================================================================

generate_training_sets = False # generated training data for machine learning model of f(TE,T,V)
train_MLP_clf = False          # train a multilayer perceptron (MLP) to approximate f(TE,T,V)
train_DT_clf = False           # train a decition tree (DT) to approximate f(TE,T,V)

save_clf = True                # save trained models to file
load_MLP_clf = False           # load MLP model
load_DT_clf = True             # load DT model

if load_MLP_clf and load_DT_clf:
  print("Chose only one model to load")
  print("set default DT...")
  load_MLP_clf = False

if generate_training_sets:
  get_trainings_data(1000,fname='data_1000.npz')
  get_trainings_data(10000,fname='data_10000.npz')
  get_trainings_data(100000,fname='data_100000.npz')
  get_trainings_data(1000000,fname='data_1000000.npz')

if train_MLP_clf:
  filename = 'MLP_model_1e6_shallower.sav'
  data = load_trainings_data('data_1000000.npz')
  data[:,1] = np.zeros([1000000,])
  #data = load_trainings_data('data_100000.npz')
  clf = MLP_train(data)
  print(clf.predict(np.array([[0,0,38,99,99,99,99,2299,199,899]])))
  print(Customer_Simulation(V=np.array([99,99,99,99,2299,199,899]),T=0,TE=0,K=0,Version=3))
  #Iteration 146, loss = 134291.32123959
  #Training loss did not improve more than tol=0.000100 for 10 consecutive epochs. Stopping.
  #Score on test set: 0.9407840489539562  
  if save_clf:
    # save the model to disk
    pickle.dump(clf, open(filename, 'wb'))

if train_DT_clf:
  filename = 'MLP_model_1e6_DT_10_300.sav'
  data = load_trainings_data('data_1000000.npz')
  data[:,1] = np.zeros([1000000,])
  clf = DT_train(data)
  print(clf.predict(np.array([[0,0,38,99,99,99,99,2299,199,899]])))
  print(Customer_Simulation(V=np.array([99,99,99,99,2299,199,899]),T=0,TE=0,K=0,Version=3))    
  if save_clf:
    # save the model to disk
    pickle.dump(clf, open(filename, 'wb'))

if load_MLP_clf:
  filename = 'MLP_model_1e6_shallower.sav'
  clf = pickle.load(open(filename, 'rb'))
  print(clf.predict(np.array([[0,0,38,99,99,99,99,2299,199,199]]))) 
  print(Customer_Simulation(V=np.array([99,99,99,99,2299,199,199]),T=0,TE=38,K=0,Version=3))
  print(clf.predict(np.array([[0,0,-9,0,0,0,0,0,59,59]])))
  print(Customer_Simulation(V=np.array([0,0,-9,0,0,59,59]),T=0,TE=38,K=0,Version=3))

if load_DT_clf:
  filename = 'MLP_model_1e6_DT_10_300.sav'
  clf = pickle.load(open(filename, 'rb'))

def model_prediction(V):
    sample = np.zeros([10,])
    sample[:2] = np.array([0,0])
    sample[2] = TE
    sample[3:10] = V
    return -1*clf.predict(sample.reshape(1, -1))

# =============================================================================
# ## Optimizer / Linear Programming 
# T = 0
# TE = -6    
# x0 = np.array([99,99,99,88,2299,199,899])
# res = minimize(model_prediction, x0, method='nelder-mead',
#            options={'xatol': 1e-8, 'disp': True})
# print(res)
# 
# res = minimize(model_prediction, x0, method='BFGS',
#                options={'disp': True})
# print(res)
# sample = np.zeros([10,])
# sample[2] = TE
# sample[3:10] = res.x.reshape(1, -1)
# print(clf.predict(sample.reshape(1, -1)))
# =============================================================================

Preisempfehlung =  np.zeros([49,2])
bounds = [(0, 299),(0, 299),(0, 299),(0, 299),(0, 1299),(0, 1299),(0, 1299)]

jj=0
for TE in range(-9,40):
    t = time.time()
    res = optimize.dual_annealing(model_prediction, bounds)
    print("predicting temperature",TE)
    Preisempfehlung[jj,0] = res.x[5]
    Preisempfehlung[jj,1] = res.x[6]
    elapsed = time.time() - t
    jj+=1
    print("took",elapsed)
    
data = np.load('Bratwurst_Wochentag_Optimal.npz')
Preisempfehlung_GT = data["Preisempfehlung"]

fig = plt.figure()
plt.plot(Preisempfehlung_GT,color='black')
plt.plot(Preisempfehlung[:,0],color='firebrick')
plt.plot(Preisempfehlung[:,1],color='darkred')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.05)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.ylim([0,600])
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Bratwurst Strategie -Wochentag-')
plt.legend(['Optimal','Bratwurst ML','Fritten ML'])
plt.savefig('OptimaleBratwurstStrategie_DT_1e6_10_300_SimAn.jpg', dpi=600)
plt.show()

plt.ylabel('sales price [pf]')
plt.xlabel('temperature [°C]')
plt.title('optimal Bratwurst strategy -weekday-')
plt.legend(['optimal','Bratwurst ML','French fries ML'])
plt.savefig('OptimaleBratwurstStrategie_DT_1e6_10_300_SimAn_EN.jpg', dpi=600)

## Beste Bratwurstsrategie als Funktion der Temperatur
Erwarteter_Gewinn = np.zeros([49,600,600])
Preisempfehlung =  np.zeros([49,2])

sample = np.zeros([10,])+ 99 # eis/cola irgendwas sinnvolles
sample[7] = 599 # zigaretten was sinnvolles... 
sample[:2] = np.array([0,0])
sample_set = np.zeros([600*600,10])
for TE in range(-9,40):
    t = time.time()
    print("predicting temperature",TE)
    jj=0
    BestGewinn = 0
    for V5 in range(0,600):
     for V6 in range(0,600):
      sample[2] = TE
      #sample[3:9] = V
      sample[8] = V5
      sample[9] = V6
      sample_set[jj,:] = sample   
      jj += 1
    Erwarteter_Gewinn[TE+9,:,:] = clf.predict(sample_set).reshape([600,600]) # ToDo check order!    
    elapsed = time.time() - t
    print("took",elapsed)

# remove negative values
Erwarteter_Gewinn[np.where(Erwarteter_Gewinn<0)]=0
np.savez('OptimaleBratwurstStrategie_DT_1e6_10_300_EN.npz',Erwarteter_Gewinn=Erwarteter_Gewinn)

# find max values 
for TE in range(-9,40):
  idx = np.argmax(Erwarteter_Gewinn[TE+9,:,:])    
  V5 , V6 = np.unravel_index(Erwarteter_Gewinn[TE+9,:,:].argmax(), Erwarteter_Gewinn[TE+9,:,:].shape)
  Preisempfehlung[TE+9,0] = V5
  Preisempfehlung[TE+9,1] = V6
    
data = np.load('Bratwurst_Wochentag_Optimal.npz')
Preisempfehlung_GT = data["Preisempfehlung"]

fig = plt.figure()
plt.plot(Preisempfehlung_GT,color='black')
plt.plot(Preisempfehlung[:,0],color='firebrick')
plt.plot(Preisempfehlung[:,1],color='darkred')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.05)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.ylim([0,600])
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Bratwurst Strategie -Wochentag-')
plt.legend(['Optimal','Bratwurst ML','Fritten ML'])
plt.savefig('OptimaleBratwurstStrategie_DT_1e6_10_300.jpg', dpi=600)

plt.ylabel('sales price [pf]')
plt.xlabel('temperature [°C]')
plt.title('optimal Bratwurst strategy -weekday-')
plt.legend(['optimal','Bratwurst ML','French fries ML'])
plt.savefig('OptimaleBratwurstStrategie_DT_1e6_10_300_EN.jpg', dpi=600)
plt.show()

#%%
# =============================================================================
# 2) Employing reinforcement learning strategies to find optimal sales prices
# =============================================================================

# E, Preisempfehlung = MC_epsilon_greedy(V=np.array([100,100,100,100,550,150,150]))
# np.savez("Preisempfehlung_RL_100_alpha_4.npz",Preisempfehlung= Preisempfehlung)
E, Preisempfehlung, Kepochs = MC_epsilon_greedy_quantized_2ndVersion(V=np.array([100,100,100,100,550,150,150]))
np.savez("Preisempfehlung_RL_quant_5_200_alpha_2_epsilon_5_2ndVersion_40kepochs.npz",Preisempfehlung= Preisempfehlung)

#%%
data = np.load('Bratwurst_Wochentag_Optimal.npz')
Preisempfehlung_GT = data["Preisempfehlung"]

fig = plt.figure()
plt.plot(Preisempfehlung_GT,color='black')
plt.plot(Preisempfehlung[:,5],color='firebrick')
plt.plot(Preisempfehlung[:,6],color='darkred')
ax = plt.gca()
ax.set_aspect('equal')
ax.set_aspect(0.05)
ax.set_xticks([0,9,19,29,39,49])
ax.set_xticklabels(['-9','0','10','20','30','40'])
plt.ylim([0,600])
#plt.gca().invert_yaxis()
plt.ylabel('Verkaufspreis [pf]')
plt.xlabel('Temperatur [°C]')
plt.title('Optimale Bratwurst Strategie -Wochentag-')
plt.legend(['Optimal','Bratwurst RL','Fritten RL'])
plt.savefig('OptimaleBratwurstStrategie_RL_quant_5_200_alpha_2_epsilon_5_2ndVersion_40kepochs.jpg', dpi=600)

plt.ylabel('sales price [pf]')
plt.xlabel('temperature [°C]')
plt.title('optimal Bratwurst strategy -weekday-')
plt.legend(['optimal','Bratwurst ML','French fries ML'])
plt.savefig('OptimaleBratwurstStrategie_RL_quant_5_200_alpha_2_epsilon_5_2ndVersion_40kepochs_EN.jpg', dpi=600)
plt.show()

fig = plt.figure()
plt.plot(Kepochs/1e2,color='black')
ax = plt.gca()
plt.ylabel('Gewinn [DM]')
plt.xlabel('epoch [#]')
plt.title('RL Performance -Wochentag-')
plt.savefig('OptimaleBratwurstStrategie_RL_perform_RL_quant_5_200_alpha_2_epsilon_2_2ndVersion_40kepochs.jpg', dpi=600)
plt.show()
