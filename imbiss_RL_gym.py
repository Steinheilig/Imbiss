# -*- coding: utf-8 -*-
"""
Machine Learning applied to defeat a 30 years old DOS game... 

Game mechanics 
"Imbiss" v. 5.4 by T. Bauer for IBM PC, Public Domain

Soft Actor Critic (SAC) Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor.
Box Actions - discrete states possible... 
https://stable-baselines.readthedocs.io/en/master/modules/sac.html

Haarnoja et al. 2018
https://arxiv.org/abs/1801.01290

Use the Custom Environments in OpenAI’s Gym

@author: Seinheilig, 2021
"""


#cd "C:\EigeneLokaleDaten\Imbiss\Python-Implementation"
from imbiss_env import ImbissEnv
env = ImbissEnv()
   
import gym
import numpy as np
import matplotlib.pyplot as plt #
from stable_baselines.sac.policies import MlpPolicy
from stable_baselines import SAC

learning_ = True 
if learning_:
 # ToDO: https://stable-baselines3.readthedocs.io/en/master/common/logger.html -> to TXT -> figure reward(timesteps)
 model = SAC(MlpPolicy, env, gamma=0.01, learning_rate = 0.001, verbose=1)  # learning rate (super low 3e-4) -> increase?
 model.learn(total_timesteps=int(1e5), log_interval=1000)
 model.save("sac_imbiss")
else:
 model = SAC.load("sac_imbiss")

#%%
obs = env.reset()
print("Start",obs)
for jj in range(20):
    action, _states = model.predict(obs)
    print("Actions:",action)
    obs, rewards, dones, info = env.step(action)
    print("State:",obs,"rewards",rewards)
    ##env.render(close=True)
    #env.render(mode='close')

#%% 
print('Test it')
for TE_ in range(49):
    action, _states = model.predict(np.array([1,TE_-9]))
    print("TE:",TE_-9,"Actions:",action)

#%% 
Preisempfehlung =  np.zeros([49,7])    
for TE in range(-9,40):
    action, _states = model.predict(np.array([1,TE]))
    print("TE:",TE,"Actions:",action)
    Preisempfehlung[TE+9,:] = action

np.savez("Preisempfehlung_SAC.npz",Preisempfehlung= Preisempfehlung)
 
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
plt.legend(['Optimal','Bratwurst (SAC)','Fritten (SAC)'])
plt.savefig('OptimaleBratwurstStrategie_SAC.jpg', dpi=600)
plt.show()    
   
#%% 
env.close()