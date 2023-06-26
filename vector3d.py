import numpy as np
import math as M
# langsam im vergleich zu pygame Vector3
def ortho_vec(vec):
   if len(vec) != 3 : print ('ortho_vec dim', len(vec), '!= 3')
   ovec = vec
   imin = 0
   if M.fabs(vec[1])<M.fabs(vec[imin]) : imin = 1
   if M.fabs(vec[2])<M.fabs(vec[imin]) : imin = 2
   length = np.sqrt(vec.dot(vec))
   ovec = vec/length
   cpmin = -ovec[imin]
   ovec = ovec*cpmin
   ovec[imin] += 1.0
   length = np.sqrt(ovec.dot(ovec))
   
   return ovec/length

def ortho_vecs(vec):
   x = ortho_vec(vec)
   length = np.sqrt(vec.dot(vec))
   z = vec/length
   y = np.cross(z, x)
   return np.array([x, y, z])

def rotate(p, v, angle):
   a = M.radians(angle)
   mat = ortho_vecs(v)
   rot = np.array([
         [ M.cos(a) , -M.sin(a), 0.0],
         [M.sin(a) , M.cos(a), 0.0],
         [ 0.0          , 0.0         , 1.0]])
   inv_mat = np.linalg.inv(mat)
   trafo = inv_mat.dot(rot)
   trafo = trafo.dot(mat)
   pp = trafo.dot(p)
   return pp
                  
