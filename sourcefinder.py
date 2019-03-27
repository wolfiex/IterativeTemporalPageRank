import numpy as np
import pandas as pd
import STPR
import STPR.dsmacc_tools as dt
from zhdf import new 

ncores = 4

filename = 'sourcetest.h5'
base   = new(filename,groupid=0,selection =['spec', 'jacsp'])
change = new(filename,groupid=1,selection =['spec', 'jacsp'])


undir_b = dt.undirect(base,ncores)
undir_c = dt.undirect(change,ncores)

net_edges = dt.net_combine(undir_b,undir_c)
print change.groupname,base.groupname


net_sp_3d = STPR.net2sparse(net_edges)
net_sp_3d.log10log=[0,0] 
net_sp_3d.log10normalise(zeronans=True)
net_sp_3d.init_pr()


out = net_sp_3d.pr(timestep = 50)

from multiprocessing import Pool


'''
Traditional Pane calculation of temporal data
'''
info = net_sp_3d.to_numpy_matrix()[1]
tsps = net_sp_3d.number_timesteps
nodes = len(info)
locations = dict([i for i in enumerate(info)])

def pagerank(i):
    pr = net_sp_3d.pr(timestep = i)
    return [pr[locations[i]] for i in range(nodes)]

pool = Pool(ncores)
results = pool.map(pagerank,range(tsps))
pool.close()

import seaborn as sns
import matplotlib.pyplot as plt
df = pd.DataFrame(results, columns=info)
sns.heatmap(df, annot=False,xticklabels=True,)
plt.show()




'''
Reversed
'''
net_sp_3d = STPR.net2sparse(net_edges)
net_sp_3d.reverse()
net_sp_3d.log10log=[0,0] 
net_sp_3d.log10normalise(zeronans=True)
net_sp_3d.init_pr()

info = net_sp_3d.to_numpy_matrix()[1]
tsps = net_sp_3d.number_timesteps
nodes = len(info)
locations = dict([i for i in enumerate(info)])

def pagerank(i):
    pr = net_sp_3d.pr(timestep = i)
    return [pr[locations[i]] for i in range(nodes)]

pool = Pool(ncores)
results = pool.map(pagerank,range(tsps))
pool.close()

import seaborn as sns
import matplotlib.pyplot as plt
df = pd.DataFrame(results, columns=info)
sns.heatmap(df, annot=False,xticklabels=True,)
plt.show()



'''
Personalised
'''
net_sp_3d = STPR.net2sparse(net_edges)
net_sp_3d.reverse()
net_sp_3d.log10log=[0,0] 
net_sp_3d.log10normalise(zeronans=True)
net_sp_3d.init_pr()



info = net_sp_3d.to_numpy_matrix()[1]
tsps = net_sp_3d.number_timesteps
nodes = len(info)
locations = dict([i for i in enumerate(info)])

personalisation = dict([[i,.1/float(nodes)] for i in info])
personalisation['O3'] = .9

def pagerank(i):
    
    pr = net_sp_3d.pr(timestep = i, personalization = personalisation)
    return [pr[locations[i]] for i in range(nodes)]

pool = Pool(ncores)
results = pool.map(pagerank,range(tsps))
pool.close()

import seaborn as sns
import matplotlib.pyplot as plt
df = pd.DataFrame(results, columns=info)
sns.heatmap(df, annot=False,xticklabels=True,)
plt.show()




