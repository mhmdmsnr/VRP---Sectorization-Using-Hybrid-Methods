import numpy as np
x = np.array([1,2,3,4,5,6])
index = np.argwhere(x==3)
y = np.delete(x, index)
print ('x: %s' %(x))
print ('y: %s' %(y))
