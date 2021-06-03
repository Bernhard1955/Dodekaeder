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
   #print('val', val)
   return val > 1.5

def rotate(p,v, sig, angle):
   pp = pygame.math.Vector3(p[0],p[1],p[2])
   vv = pygame.math.Vector3(v[0],v[1],v[2])
   vv.normalize()
   pp = pp.rotate(sig*angle,vv)
   p[0] = pp[0]
   p[1] = pp[1]
   p[2] = pp[2]
   return p

class Dodekaeder():

   def init(self):
      dodeka = polygons()
      self.sides = get_side_plgs()
      self.centers = get_centers()
      self.plgs = get_plgs()
      #print ('self.sides', np.shape(self.sides))
      #print ('self.centers', np.shape(self.centers))
      #print ('self.plgs', np.shape(self.plgs))

   def reset(self):
      self.init()

   def get_side_plgs(self):
      return self.centers, self.sides

   def get_centers(self):
      return self.centers

   def get_angle(self):
      return 72

   def rotate_side(self, side, sig,angle):
      vec = self.centers[side]
      for plgs in self.plgs:
         for plg in plgs:
            if (to_rot(plg, vec)):
               #print ('side = ',side, ' sig = ', sig)
               for pt in plg:
                  pt = rotate(pt,vec,sig,angle) 

   def get_plgs(self):  
      return self.plgs

   def init_plgs(self,plgs):
      self.plgs=plgs
   
   def store(f):
      json.dump([plgs],f)
