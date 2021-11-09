import numpy as np
import math as M
from polygons import *
import json

def to_rot(plg,vec):
   center = np.zeros(3, np.float)
   for j  in range(len(plg)-1):
      center = center + plg[j] 
   val = center.dot(vec)
   val = val / (len(plg)-1)
   return val > 1.5

def ROTATE(p,v, sig, angle):
   a = 1.0/np.linalg.norm(v)*v
   r = np.zeros((3,3))
   an = -sig*angle/180 * M.pi
   sn = M.sin(an)
   cs = M.cos(an)
   r[0][0],r[0][1],r[0][2]=a[0]*a[0]*(1-cs)+cs,a[0]*a[1]*(1-cs)-a[2]*sn,a[0]*a[2]*(1-cs)+a[1]*sn
   r[1][0],r[1][1],r[1][2]=a[1]*a[0]*(1-cs)+a[2]*sn,a[1]*a[1]*(1-cs)+cs,a[1]*a[2]*(1-cs)-a[0]*sn
   r[2][0],r[2][1],r[2][2]=a[2]*a[0]*(1-cs)-a[1]*sn,a[2]*a[1]*(1-cs)+a[0]*sn,a[2]*a[2]*(1-cs)+cs
   p[0:3] = p.dot(r)
   return 

class Dodekaeder():

   def INIT(self):
      dodeka = polygons()
      self.sides = SIDE_PLGS()
      self.centers = CENTERS()
      self.plgs = PLGS()

   def RESET(self):
      self.INIT()

   def GET_SIDE_PLGS(self):
      return self.centers, self.sides

   def GET_CENTERS(self):
      return self.centers

   def GET_ANGLE(self):
      return 72

   def ROTATE_SIDE(self, side, sig,angle):
      vec = self.centers[side]
      for plgs in self.plgs:
         for plg in plgs:
            if (to_rot(plg, vec)):
               for pt in plg:
                  ROTATE(pt,vec,sig,angle) 

   def GET_PLGS(self):  
      return self.plgs

   def GET_PLGS(self):  
      return self.plgs
