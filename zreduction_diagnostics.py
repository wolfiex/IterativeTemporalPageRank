''' 
Insparation from using the google csc_matrix
https://github.com/networkx/networkx/blob/2db5f8663deacc501c7472c3a60884a2ca8be45a/networkx/algorithms/link_analysis/pagerank_alg.py
'''


from pathos.multiprocessing import ProcessPool
import time
import numpy as np
import pandas as pd

import STPR

ncores = 50





def undirect(self):
    '''
    Remove directional links between species by finding the net weight of the jacobian
    '''

    dct={}
    specs = self.spec.columns
    iterate = []
    for i in specs:
        for j in specs:
            if i==j: break
            iterate.append(list(set([i,j])))

    print iterate


    self = self.jacsp.compute()


    def net(d):
        ret = []
        for n in d:
            total =[]
            try: total.append(self['%s->%s'%(n[0],n[1])])
            except:None
            try: total.append(-self['%s->%s'%(n[1],n[0])])
            except:None

            if len(total) > 0 :
                ret.append(['->'.join(n), sum(total)])
        return ret

    dct = ProcessPool(nodes=ncores).amap(net,np.array_split(iterate,ncores))

    while not dct.ready():
         time.sleep(5); print(".")

    dct = dct.get()

    return dict([i for j in dct for i in j])


'''
import zhdf
a = zhdf.new("../lhs_spinup_training.h5")
a.rm_spinup()
b = zhdf.new("../lhs_spinup.h5")
b.rm_spinup()

a = undirect(a)
b = undirect(b)


lumped = '../mechanisms/lumped_formatted_CRI_FULL_2.2_inorganics_True.kpp'
import re
header = a.keys()
lumped = open(lumped).readlines()
lumped = re.findall(r'(LMP\d+): ([\w,]+)',''.join(lumped))

print len(header)
newheader = []

for n,l in lumped:
    sub = re.compile(r'\b(%s)\b'%(l.replace(',','|')))
    header = ['->'.join(list(set( sub.sub(n, i).split('->')))) if sub.match(n) else i for i in header]


a = dict(zip(header,a.values()))
a = pd.concat(a.values(),axis=1)
a.columns=header
a = a.groupby(by=a.columns,axis=1).agg(np.sum)

b = pd.concat(b.values(),axis=1)


keep = list(set(a.keys()) & set(b.keys()))
dismiss = set(a.keys()) ^ set(b.keys())


print('ignoring',dismiss)


net_edges = b[keep].divide(a[keep],axis=1)
'''


nsp.log10normalise(zeronans = True)
print nsp


'''
import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()


ts = edges.index[0]

selection = edges.loc[ts,:]
mn = selection.min()
mx = selection.max()

for e in edges.columns:
        split = e.split('->')
        G.add_edge(split[0],split[1],weight=(1-((edges.loc[ts,e]-mn)/(mx-mn)))**8)

G.remove_edges_from(G.selfloop_edges())

pos = nx.spring_layout(G)  # positions for all nodes

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)


elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]
# edges
nx.draw_networkx_edges(G, pos, edgelist=elarge,
                       width=6)
nx.draw_networkx_edges(G, pos, edgelist=esmall,
                       width=6, alpha=0.5, edge_color='b', style='dashed')

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

plt.axis('off')
plt.show()
'''
