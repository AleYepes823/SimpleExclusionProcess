import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

Results = pd.read_excel('RPaseoSinai2.xlsx', index_col = 0)
e_Results = pd.read_excel('ePaseoSinai2.xlsx', index_col = 0)

Times = np.arange(100,50001,100)

cmap = get_cmap(len(Results.keys())+1)

for i,Delta in enumerate(Results):
    delta =float(Delta.replace('delta=',''))
    plt.plot(Times,Results[Delta],'-',c = cmap(i), label = rf'$\delta = {delta:.2f}$')
plt.legend()
plt.xlabel('Evolution Time')
plt.ylabel(r'$\Delta x^2$')
plt.grid(ls = ':', c = 'k', alpha = 0.3)
plt.savefig('SinaiEvolution.png',bbox_inches = 'tight')
plt.show()
