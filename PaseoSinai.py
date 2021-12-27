import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from uncertainties import ufloat
import time

np.random.seed(2021)

#TODO Parameters
Time = 50001 #? Simulation Time
N = Time*6+1 #? number of places in the chain
Nparticles = 1 #? number of particles in the system
DeltaTime = 0.1 #? Time Delta grid
Niter = int((Time+DeltaTime)//DeltaTime) #? Number of simulation iterations
beta = 0.5 #? numpy exponential distribution beta parameter, beta = 1/lambda

#TODO initial por Generator
ParticlePosition0 = int((N-1)/2)


def GenerateRandomJumps(Time, beta):
    """this function will generate the particle clocks
    that will determine the time of the particle to jump

    Args:
        Niter (int): number of simulation iterations
        s0 (numpy array): initial state of the system
        lam (float): poisson parameter
    
    Returns:
        JumpTimes (list of list [matrix]): times of the particle to jump
    """

    JumpTimes = [0.0] #? list of times to jump

    while JumpTimes[-1] < Time:
        newdelta = np.random.exponential(beta)
        if JumpTimes[-1] + newdelta <= Time:
            JumpTimes.append(JumpTimes[-1] + newdelta)
        elif JumpTimes[-1] + newdelta > Time:
            del JumpTimes[0]
            break

    return np.array(JumpTimes)



def simulate(Time,DeltaTime,beta, ParticlePosition0, TimeData = 100):
    """This function is the one encharged of simulating
    the simple exclusion process

    Args:
        Time (int): Number of iterations for the simulation
        Positions (array): Positions of the numbered particles (initial state)
        s0 (array): initial state of the system
        N (int): number of places in the chain
        lam (int): poisson parameter
    """
    ParticlePosition = ParticlePosition0
    Niter = int((Time+DeltaTime)//DeltaTime)
    TimeData /=  DeltaTime

    JumpTimes = GenerateRandomJumps(Time,beta)//DeltaTime + 1
    JumpTimes.astype(int)

    Results = {}

    for i in range(1,Niter):
        if i in JumpTimes:
            proba = np.random.random()
            if proba < pleft[ParticlePosition]: next = -1
            elif proba > pleft[ParticlePosition]: next = +1
            ParticlePosition += next
        if i%TimeData == 0:
            Results[f't={int(i*100/TimeData):d}'] = ParticlePosition
    return pd.Series(Results)



Deltas = np.linspace(0,1,num = 11,endpoint=True)*0.5
# Times = np.arange(1,30)*100

t0 = time.time()
Results = pd.DataFrame()
for delta in Deltas:
    delta = round(delta,2)
    pright = 1/2 + delta*np.random.uniform(low = -1.0, high = 1.0, size = N) #? probability of the particle jumping right [0.0,1.0)
    pleft = 1 - pright #? probability of the particle jumping left
    simulation_results = pd.DataFrame()
    for i in range(150):
        Evolucion = simulate(Time,DeltaTime,beta,ParticlePosition0)
        Evolucion.to_excel(f'DatosSinai/Iteracion{i+1:0>3d}.xlsx', engine = 'openpyxl')
        simulation_results[f'iter{i+1}'] = Evolucion
    Results[f'delta={delta}'] = simulation_results.var(axis = 1)


Results.to_excel('RPaseoSinai3.xlsx', engine = 'openpyxl')
print(time.time()-t0)
print(Results)
