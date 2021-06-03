import pygame 
import numpy as np
from polygons import *
import json

def to_rot(plg,vec):
   center = np.zeros(3, np.float)
   for j  in range(0,len(plg)-1):
      center = center + plg[j] 
   val = center[0]*vec[0]+center[1]*vec[1]+center[2]*vec[2]
   val = val / (len(plg)-1)
   return val > 1.5

def ROTATE(p,v, sig, angle):
   pp = pygame.math.Vector3(p[0],p[1],p[2])
   vv = pygame.math.Vector3(v[0],v[1],v[2])
   vv.normalize()
   pp = pp.rotate(sig*angle,vv)
   p[0] = pp[0]
   p[1] = pp[1]
   p[2] = pp[2]
   return p

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
                  pt = ROTATE(pt,vec,sig,angle) 

   def GET_PLGS(self):  
      return self.plgs

   def GET_PLGS(self):  
      return self.plgs
