'''
A cumelative page rank algorith for errors of a temporal network.
'''
import multiprocessing


class Sparse3D:
  '''
  A 3 Dimentional sparse matrix represenatation.
  
  Autoinput:
      adjacency - n x n matrix of value items (items can be anything)
      names - list of names (e.g. G.nodes())
   
  onnone:
      value or object to return when a non-existant link is summoned.
  '''
  def __init__(self,adjacency_matrix = None, names = None, onnone=0):
    self.data = {}
    self.names = None
    self.onnone = onnone
    
    if adjacency_matrix != None:
      vals=len(adjacency_matrix)
      if names!= None:
        assert(val == len(names))
        self.names = names
      else:
        self.names=range(val)

      for i in range(vals):
          for j in range(vals):
                dummy  = adjacency_matrix[i,j]
                if dummy: self.data[(names[i],names[j])] = dummy
      
  def add(self, source,target, values):
    self.data[(source,target)] = values

  def read(self, source,target):
    try:
      value = self.data[(source,target)]
    except KeyError:
      value = self.onnone
    return value
