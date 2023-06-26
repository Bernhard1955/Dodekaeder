import numpy as np

x = np.zeros(5)
print  (x)
for i in range(len(x)) :
   print (i)

x = np.array([4,0,3])
print (np.linalg.norm(x))
rot = np.zeros((3,3))
rot[0][0] =1
