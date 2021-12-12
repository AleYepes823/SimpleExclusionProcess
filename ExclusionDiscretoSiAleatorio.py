import numpy as np
import matplotlib.pyplot as plt

# np.random.seed(2021)

#TODO Parameters
N = 100 #? number of places in the chain
Nparticles = 20 #? number of particles in the system
Niter = 300 #? number of simulation iterations

#TODO initial por Generator
s0 = np.ones(shape = Nparticles)
s = np.zeros(shape = N-Nparticles)
s0 = np.append(s0,s)
np.random.shuffle(s0)#? initial state 
Positions = s0.astype('float') #? numbered initial state
count = 1
for n in range(N):
    if Positions[n] == 1.:
        Positions[n] = count
        count = count + 1

#TODO jumpling probability definition
pright = np.random.random(size = len(s0)) #? probability of the particle jumping right
pleft = 1 - pright #? probability of the particle jumping left


def CanJump(Positions, n, side, N = N):
    """this function will determine whether
    the particle can jump to the place the
    the markov chain has desided

    Args:
        s (numpy array): current state of the system
        n (int): place number of the particle to jump
        side (string): side desided of the particle to jump to
    
    Returns:
        switch (bool): whether the particle can jump
    """

    next = None
    if side == 'left': next = -1
    elif side == 'right': next = 1
    switch = None

    NextPos = n + next
    NextPos %= N
    if Positions[NextPos] != 0: switch = False
    elif Positions[NextPos] == 0: switch = True

    return switch


def GenerateRandomJumps(Niter, s0, lam):
    """this function will generate the particle clocks
    that will determine the time of the particle to jump

    Args:
        Niter (int): number of simulation iterations
        s0 (numpy array): initial state of the system
        lam (float): poisson parameter
    
    Returns:
        JumpTimes (list of list [matrix]): times of the particle to jump
    """

    Nparticles = s0.sum()
    JumpTimes = []

    for i in range(Nparticles):
        Times = np.random.poisson(lam = lam,size = int(Niter/lam+10))
        JumpTimesGen = [0]
        for j in range(int(Niter/lam+10)):
            TimeSum = JumpTimesGen[-1]+Times[j]
            if TimeSum <=Niter:
                JumpTimesGen.append(TimeSum)
            else:
                del JumpTimesGen[0]
                JumpTimes.append(JumpTimesGen)
                break
    JumpTimes = np.array(JumpTimes)
    return JumpTimes, Nparticles



def simulate(Niter, Positions, s0, N):
    """This function is the one encharged of simulating
    the simple exclusion process

    Args:
        Niter (int): Number of iterations for the simulation
        Positions (array): Positions of the numbered particles (initial state)
        s0 (array): initial state of the system
        N (int): number of places in the chain
        lam (int): poisson parameter
    """
    s = s0
    Nparticles = s0.sum()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    line, = ax.plot(np.arange(1,N+1),s,'bo')

    ax.set_xlim(-0.2, N+1.2)
    ax.set_ylim(0.8,1.2)
    fig.suptitle(f'Iteration Number {0}')
    plt.axis('off')

    for i in range(1,Niter+1):
        ParticleToJump = np.random.randint(1,Nparticles+1)
        proba = np.random.random()
        ParticlePosition = int(np.where(Positions == ParticleToJump)[0])
        if proba < pleft[ParticlePosition]: Direction = 'left'; next = -1
        elif proba > pleft[ParticlePosition]: Direction = 'right'; next = +1
        switch = CanJump(Positions, ParticlePosition, Direction)
        if switch:
            NextPos = ParticlePosition+next
            NextPos %= N
            Positions[NextPos] = Positions[ParticlePosition]
            Positions[ParticlePosition] = 0
            s[NextPos] = 1
            s[ParticlePosition] = 0
        line.set_ydata(s)
        fig.suptitle(f'Iteration Number {i}')
        fig.canvas.draw()
        plt.pause(0.20)
        fig.canvas.flush_events()


simulate(Niter, Positions, s0, N)