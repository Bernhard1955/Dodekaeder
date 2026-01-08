# -*- coding: UTF-8 -*- 

# Import modules 
import json
import copy
from tkinter import *
import tkinter.filedialog
import optparse
import math as M
import random
import numpy as np
import pygame 
from pygame.locals import * 
from pygame._sdl2 import touch


def PRINT(*a):
   if DEBUG: print(*a)

class Eventhandling():

   def __init__(self, rubik,verbose):
      self.V = verbose
      global DEBUG
      DEBUG = verbose
      self.rubik = rubik

      pygame.init()
      size_x=1200
      size_y=800
      screensize = (size_x,size_y)
      sc = pygame.display.set_mode(screensize,RESIZABLE)
      self.screen = sc
      self.shift=False
      self.ctrl=False
      self.rot_alpha=0
      self.steps =[]
      self.text = []
      self.record = 0
      self.store = []
      self.rs = -1
      self.strg_c = []
      self.rotkey = {}

      self.side = -1
      self.center = None
      self.mouse = [0,0]
      self.sign = 0

      self.farben = []
      self.centers = self.rubik.GET_CENTERS()
      self.farben = self.rubik.GET_COLORS()
      self.T = touch.get_num_devices() > 0
      self.RESIZE()

      self.mat = np.eye(3,3)
      self.mat[0][0] = self.mat[1][1] = self.mat[2][2]= 1.0
      self.scl = self.mat
      self.mat_last = self.mat
      self.alpha = 0.0
      self.beta = 0.0
      self.gamma = 0.0
      self.delta = 24
      self.help = False
      PRINT('num_devices = ',touch.get_num_devices())
      self.PLOT()

   def INIT_TOUCH(self):
      self.device = touch.get_device(0)
      test = True
      self.nf = 0
      self.delta = 7
      sx = self.size_x
      sy = self.size_y
      dx = self.grid_x
      dy = self.grid_y
      b1 = [[sx-12*dx,1],[sx-7*dx,1+2*dy]]
      b2 = [[sx- 7*dx,1],[sx-1*dx,1+2*dy]]
      b3 = [[sx-12*dx,sy-2*dy+1],[sx-7*dx,sy-1]]
      b4 = [[sx- 7*dx,sy-2*dy+1],[sx-1*dx,sy-1]]
      b5 = [[1,sy-2*dy+1],[5*dx,sy-1]]
      b6 = [[5*dx,sy-2*dy+1],[10*dx,sy-1]]
      b7 = [[sx-22*dx,sy-2*dy+1],[sx-17*dx,sy-1]]
      b8 = [[sx-17*dx,sy-2*dy+1],[sx-12*dx,sy-1]]
      b9 = [[sx- 7*dx,1+2*dy],[sx-1*dx,1+4*dy]]
      b9 = [[1,sy-4*dy+1],[5*dx,sy-2*dy+1]]
      self.B = [b1,b2,b3,b4,b5,b6,b7,b8,b9]
      t1 = 'Rot_left'
      t2 = 'Rot_right'
      t3 = 'CTRL-C'
      t4 = 'CTRL-V'
      t5 = 'Store'
      t6 = 'Open'
      t7 = 'CTRL-Z'
      t8 = 'Reset'
      t9 = 'Rotate'
      self.Text = [t1,t2,t3,t4,t5,t6,t7,t8,t9]

   def RESIZE(self):
      self.size_x = self.screen.get_width()
      self.size_y = self.screen.get_height()
      self.mid = [float(self.size_x)/2.0, float(self.size_y)/2.0 ]
      self.size = float(min(self.size_x, self.size_y))
      r = np.linalg.norm(self.centers[0])
      self.scale = 0.3/r*self.size
      self.grid_x =  max(50,self.size_x/55) #self.size_x/20
      self.grid_y =  max(50,self.size_x/55) #self.size_y/20
      if self.T:
         self.INIT_TOUCH()

   def WAIT(self):
      PRINT ('Wait')
      while True:
         event = pygame.event.wait()
         if event.type == QUIT:
            pygame.quit()
            return
         elif event.type == WINDOWSIZECHANGED: #resize
            PRINT('Resize Screen 2')
            self.RESIZE()
            self.PLOT()
      
         if self.T:
            self.TOUCH_CONTROL(event)
            
         else:   
            self.MOUSE_CONTROL(event)
      return   

   def TOUCH_CONTROL(self,event):
      try: 
         nf = pygame._sdl2.touch.get_num_fingers(self.device)
      except:
         nf = 0
      if event.type == FINGERMOTION:
         if nf == 2:
            try:
               #finger = touch.get_finger(device,0)
               ed = event.dict
               mouse = [ed['x']*self.size_x, ed['y']*self.size_y]
               mouse_move = [ed['dx']*self.size_x, ed['dy']*self.size_y]
               self.ROT(mouse, mouse_move)
               self.PLOT()
            except:
               pass
         elif nf == 1 and self.side >=0 :
            finger = touch.get_finger(self.device,0)
            mouse = [finger['x']*self.size_x, finger['y']*self.size_y]
            self.sign = 1
            v0 = [self.mouse[0]-self.center[0], self.mouse[1]-self.center[1]]
            v1 = [mouse[0]-self.center[0], mouse[1]-self.center[1]]
            cross = v0[0]*v1[1] - v0[1]*v1[0]
            if cross < 0 : self.sign = -1
            PRINT('cross=', cross, self.sign, v0, v1)
      if event.type == FINGERUP:
         PRINT('nf= ', nf)
         if self.side > -1 and nf == 0 and self.sign != 0:
            step = [self.side,self.sign]
            self.ROTADE_SIDE(step)
            if len(self.steps)>0 and self.steps[-1][0] == step[0] and self.steps[-1][1] == -step[1]:
               self.steps.pop()
            else:
               self.steps.append(step)
            self.side = -1
            self.sign = 0# reset side
            self.PLOT()

      if event.type == FINGERDOWN:
         if nf > 0:
            finger = touch.get_finger(self.device,0)
            PRINT ('finger', finger)
            mouse = [finger['x']*self.size_x, finger['y']*self.size_y]
         if nf == 1:
            side = -1
            button_pressed = [False,True,False]
            side, center = self.GET_SIDE(mouse,button_pressed)
            if side > -1 : 
               PRINT ('side, center', side, center)
               center2d = self.PLG2D([center])
               PRINT('center=', center, center2d[0], mouse)
               self.side = side
               self.center = center2d[0] 
               self.mouse = [int(mouse[0]), int(mouse[1])]
            else:
               cmd = self.GET_CMD(mouse)
               if cmd == -1 : self.CONTROL(mouse,[True,False,False])
               if nf == 1:
                  if cmd == 4: self.CTRL_S()
                  if cmd == 5: self.CTRL_O()
                  if cmd == 6: self.CTRL_Z()
                  if cmd == 7: self.CTRL_X()
               
         elif nf == 2 :
            self.side = -1
            finger2 = touch.get_finger(self.device,1)
            mouse2 = [finger2['x']*self.size_x, finger2['y']*self.size_y]
            cmd = self.GET_CMD(mouse2)
            side = -1
            if cmd == 0 or cmd == 1:
               if cmd == 0 : rot = 0
               if cmd == 1 : rot = 2
               pressed = 3*[False]
               pressed[rot]=True
               side, center = self.GET_SIDE(mouse,pressed)
               if side >= 0 : return
            elif cmd == 2 :#ctrl_c
               self.CTRL_C(mouse)
            elif cmd == 3 :#ctrl_c
               self.CTRL_V(mouse)

            if side < 0:
               cmd = self.GET_CMD(mouse)
               if cmd == 0 or cmd == 1:
                  if cmd == 0 : rot = 0
                  if cmd == 1 : rot = 2
                  pressed = 3*[False]
                  pressed[rot]=True
                  side, center = self.GET_SIDE(mouse2,pressed)
               elif cmd == 2 :#ctrl_c
                  self.CTRL_C(mouse2)
               elif cmd == 3 :#ctrl_c
                  self.CTRL_V(mouse2)

   def GET_CMD(self, mouse):
      for i in range(len(self.B)):
         b = self.B[i]
         if b[0][0] < mouse[0] and mouse[0] < b[1][0]:
            if b[0][1] < mouse[1] and mouse[1] < b[1][1]:
               PRINT('button ',i,'pressed')
               return i
      return -1


   def MOUSE_CONTROL(self,event):
      mouse = pygame.mouse.get_pos()
      mouse_move = pygame.mouse.get_rel()
      button_pressed = pygame.mouse.get_pressed()
      
      if event.type == KEYDOWN: # Key pressed
         taste = pygame.key.name(event.key)
         sides='kiolmj'
         if self.ctrl:
            if taste == 'x':
               self.CTRL_X()
            elif taste == 'z':
               self.CTRL_Z()
            elif taste == 'c':
               self.CTRL_C(mouse)
            elif taste == 'v':
               self.CTRL_V(mouse)
            elif taste == 's':
               self.CTRL_S()
            elif taste == 'o':
               self.CTRL_O()
         if taste in '1234567890':
            self.RANDOM(taste)
         # rotate side with keyboard kiolmj
         elif self.shift:
            if taste in sides:
               #side = sides.find(taste)
               side = self.rotkey[taste]
               PRINT('side--- ',side, taste, self.rotkey)
               sign = 1
               step = [side,sign]   
               self.ROTADE_SIDE(step, True)
         else:
            if taste in sides and taste in self.rotkey.keys() :
               side = self.rotkey[taste]
               PRINT('side--- ',side, taste, self.rotkey)
               sign = -1
               step = [side,sign]   
               self.ROTADE_SIDE(step, True)
            elif taste =='f1':
               self.PLOT(taste)
            
         if 'shift' in taste:  
            self.shift = True
         if 'ctrl' in taste:  
            self.ctrl = True
         PRINT('taste pressed',taste, self.shift,self.ctrl)
         return
      if event.type == KEYUP: # Key releasde
         taste = pygame.key.name(event.key)
         if 'shift' in taste:  
            self.shift = False
         if 'ctrl' in taste:  
            self.ctrl = False
         PRINT('taste release',taste, self.shift,self.ctrl)
         return
      
      if event.type == 1025 and button_pressed[0] :
         if self.CONTROL(mouse, button_pressed):
            return
      
      if self.shift:
         if button_pressed[1]:
            self.ROT(mouse, mouse_move)
            PRINT ('Wait, ROT')
            self.PLOT()
      elif event.type == MOUSEBUTTONDOWN and button_pressed[1]:
         side, center = self.GET_SIDE(mouse,button_pressed)
         if side > -1 : 
            center2d = self.PLG2D([center])
            PRINT('center=', center, center2d[0], mouse)
            self.side = side
            self.center = center2d[0] 
            self.mouse = [mouse[0], mouse[1]]
      elif event.type == MOUSEMOTION and button_pressed[1] and self.side >=0:
         self.sign = 1
         v0 = [self.mouse[0]-self.center[0], self.mouse[1]-self.center[1]]
         v1 = [mouse[0]-self.center[0], mouse[1]-self.center[1]]
         cross = v0[0]*v1[1] - v0[1]*v1[0]
         if cross < 0 : self.sign = -1
         PRINT('cross=', cross, self.sign, v0, v1)
      elif event.type == MOUSEBUTTONUP and button_pressed[1]==False and self.side >=0:
         if self.side > -1 and self.sign != 0:
            step = [self.side,self.sign]
            self.ROTADE_SIDE(step)
            if len(self.steps)>0 and self.steps[-1][0] == step[0] and self.steps[-1][1] == -step[1]:
               self.steps.pop()
            else:
               self.steps.append(step)
            self.side = -1
            self.sign = 0# reset side
            self.PLOT()
      elif event.type == MOUSEBUTTONDOWN and (button_pressed[0] or button_pressed[2]):
         side, center = self.GET_SIDE(mouse,button_pressed)

   def GET_SIDE(self,mouse, button_pressed):
      #PRINT ( mouse, mouse_move)
      centers,plgs = self.rubik.GET_SIDE_PLGS()
      i=-1
      side = -1
      center = None
      for plg3d in plgs:
         i += 1
         if ( self.TO_PAINT(plg3d)):
            pg2d = self.PLG2D(plg3d)
            if self.IN_PLG(mouse,pg2d) : 
               side = i
               break
      if side >= 0:
         PRINT ('Wait, GET_SIDE', side)
         center = centers[side]
         if button_pressed[1]:
            return side, center
         sign = 1
         if button_pressed[0]: sign = -1
         step = [side,sign]   
         self.ROTADE_SIDE(step)
         if len(self.steps)>0 and self.steps[-1][0] == step[0] and self.steps[-1][1] == -step[1]:
            self.steps.pop()
         else:
            self.steps.append(step)
         PRINT ('len(steps)', len(self.steps))
         self.PLOT()
      return side, center

   def TO_PAINT(self, plg):
      v1 = plg[1]-plg[0]
      v2 = plg[2]-plg[1]
      v3 = [(v1[1]*v2[2] - v1[2]*v2[1]), (v1[2]*v2[0] - v1[0]*v2[2]), (v1[0]*v2[1] - v1[1]*v2[0])]
      v1 = self.mat.dot( plg[1])   
      v3 = self.mat.dot(v3)
      if v1.dot(v3) >0 :
         # PRINT ('+')
         return v3[2] >0
      else:
         # PRINT ('-')
         return v3[2] <0

   def PLG2D(self,plg3d):
      pg2d = []
      for pt in plg3d:
         PT2D = self.PT2D(pt)
         pg2d.append( PT2D ) 
      return pg2d

   def PT2D(self,pt3d):
      p3d = self.mat.dot(pt3d)
      pt = [int( self.mid[0]+p3d[0]*self.scale),int(self.mid[1]+p3d[1]*self.scale)]
      return pt

   def IN_PLG(self,m,pg2d):
      last = 0
      for i in range(0,len(pg2d)) :
         p0 = pg2d[i]
         p1 = pg2d[(i+1)%len(pg2d)]   
         v0 = (p0[0]-m[0],p0[1]-m[1])
         v1 = (p1[0]-m[0],p1[1]-m[1])
         l = v1[0]*v0[1] - v1[1]*v0[0]
         if l*last <0 : return False
         if l != 0 : last = l
      return True 

   def PLOT(self, taste = ''):
      self.screen.fill((178,178,178))
      plgs = self.rubik.GET_PLGS()
      self.PLOT_PG(plgs)
      self.PLOT_STEPS()
      self.PLOT_STATUS()
      if taste == 'f1':
         self.HELP()
      #self.PLOT_CIRCLE()
      pygame.display.flip()

   def PLOT_PG(self, pg):
      schwarz = pygame.Color(0,0,0)
      i=0
      for plgs in pg:
         color = self.farben[i]
         i +=1
         for plg3d in plgs:
            if self.TO_PAINT(plg3d) :
               pg2d = self.PLG2D(plg3d)   
               pygame.draw.polygon(self.screen, color, pg2d, 0)
               pygame.draw.polygon(self.screen, (0,0,0), pg2d, 4)
      
      first = True
      c = self.strg_c
      if len(c) > 1:
         for ij in c:
            PRINT( 'PLOT_PG ij', ij)
            plg3d = pg[ij[0]][ij[1]]
            if self.TO_PAINT(plg3d):
               pg2d = self.PLG2D(plg3d)   
               color = self.farben[ij[0]]
               if first:
                  first = False
                  c =[0,0,0] 
                  for i in range(3):
                     c[i] = 0.8*(color[i] + int(0.5*(255-color[i])))
                  color = (c[0],c[1],c[2])   
               pygame.draw.polygon(self.screen, color, pg2d, 0)
               pygame.draw.polygon(self.screen, (255-color[0],255-color[1],255-color[2]), pg2d, 4)
      
   def PLOT_STEPS(self):
      dx =  self.grid_x
      x = 2*dx
      self.plot_steps(self.steps, self.size_x)
      if self.record : self.plot_steps(self.steps[self.rs:], dx)
      if len(self.store) > 0 :
         PRINT ( 'print len(self.store)', len(self.store[0]))
      for  steps in self.store:
         self.plot_steps(steps, x)
         x += dx

   def plot_steps(self, steps, x):
      dx = self.grid_x/2
      dy = self.grid_y/2
      xl = x -1.0*dx
      xr = x -0.5*dx
      ys = self.grid_y
      r = 0.4*dy
   
      PRINT ( 'print len(stps)', len(steps))
      PRINT (steps)
      for step in steps:
         if step[1] == -1: x=xl
         else: x=xr
         ys +=dy
         center = (x, ys)
         PRINT( 'step= ', step, 'center= ', center)
         pygame.draw.circle(self.screen, self.farben[step[0]], center, r)

   def ROTADE_SIDE(self, step, append=False):
      PRINT ('ROTADE_SIDE')
      delta = self.delta
      angle = self.rubik.GET_ANGLE()
      da = angle/delta
      for i in range(delta):
         self.rubik.ROTATE_SIDE(step[0],step[1],da)
         self.PLOT()
      if append :
         if len(self.steps)>0 and self.steps[-1][0] == step[0] and self.steps[-1][1] == -step[1]:
            self.steps.pop()
         else:
            self.steps.append(step)
         if self.V:
            PRINT ('len(steps)', len(self.steps))
         self.PLOT()

   def ROT(self,mouse, mv):
      d = (mouse[0]-self.mid[0])*(mouse[0]-self.mid[0])+(mouse[1]-self.mid[1])*(mouse[1]-self.mid[1])

      if d < self.size_y*self.size_y*0.17:
         self.rot_alpha = 0
      else:
         self.rot_alpha = 3
      PRINT('self.rot_alpha', self.rot_alpha)

      if self.rot_alpha == 0 or self.rot_alpha == 1:
         self.alpha = float(mv[0])/450*M.pi
      if self.rot_alpha == 0 or self.rot_alpha == 2:
         self.beta  = float(mv[1])/300*M.pi
      if self.rot_alpha == 3 :
         delta  = M.sqrt(float(mv[1]*mv[1]+mv[0]*mv[0]))/400*M.pi
         if ( (mouse[0]-self.mid[0])*mv[1] - (mouse[1]-self.mid[1])*mv[0] ) > 0:
            delta = -delta
         self.gamma =delta   
      rot_x = np.eye(3,3)
      if self.rot_alpha == 0 or self.rot_alpha == 1:
         rot_x[1][1]= rot_x[2][2]=M.cos(self.beta)
         rot_x[1][2]=M.sin(self.beta)
         rot_x[2][1]= -rot_x[1][2]
         rot_x[0][0]= 1.0

      rot_y = np.eye(3,3)
      if self.rot_alpha == 0 or self.rot_alpha == 2:
         rot_y[1][1]= 1.0
         rot_y[0][0]= rot_y[2][2]=M.cos(self.alpha)
         rot_y[0][2]=M.sin(self.alpha)
         rot_y[2][0]= -rot_y[0][2]

      rot_z = np.eye(3,3)
      if self.rot_alpha == 3:
         rot_z[2][2]= 1.0
         rot_z[0][0]= rot_z[1][1]=M.cos(self.gamma)
         rot_z[0][1]=M.sin(self.gamma)
         rot_z[1][0]= -rot_z[0][1]
      self.mat = rot_x.dot(rot_y.dot(rot_z.dot(self.mat))) 
      # map rubik side to leter kiolmj
      centers = self.rubik.GET_CENTERS()
      centers = [self.mat.dot(centers[i]) for i in range(len(centers))]
      leters = 'kiolmjswedxa-----'
      visib = []
      for i in range(len(centers)):
         if centers[i][2] > 0 :
            visib.append([centers[i][2],i])
      visib.sort()
      for x in visib[0:-1]:
         x[0] = (M.atan2(centers[x[1]][1], centers[x[1]][0])+7*M.pi/10)%(2*M.pi)
      self.rotkey = {}
      PRINT(visib)
      self.rotkey[leters[0]] = visib.pop()[1]
      visib.sort()
      PRINT(visib)
      for i in range(len(visib)):
         PRINT(i,leters[i+1])
         self.rotkey[leters[i+1]] = visib[i][1]
      PRINT (self.rotkey)


   def PLOT_STATUS(self):
      c = (self.grid_x/2, self.grid_y/2)
      r = self.grid_x/3
      frb1 = pygame.Color(255,0,0)
      frb2 = pygame.Color(128,0,0)
      frb3 = pygame.Color(192,0,0)
      if ( self.record == True) :
         f1 = frb1
         f2 = frb2
      else:
         f2 = frb1
         f1 = frb2

      pg2d = [[c[0]-r,c[1]+r],[c[0]-r,c[1]-r],[c[0]+r,c[1]-r],[c[0]+r,c[1]+r]]
      pygame.draw.polygon(self.screen, frb3, pg2d, 0)
      pygame.draw.lines(self.screen, f2, False, pg2d[:3], 4)
      pg2d = [[c[0]-r,c[1]+r],[c[0]+r,c[1]+r],[c[0]+r,c[1]-r],[c[0]-r,c[1]-r]]
      pygame.draw.lines(self.screen, f1, False, pg2d[:3], 4)

      farbe = pygame.Color(255,0,0)
      cx = self.size_x-self.grid_x/2
      cy = self.grid_y/4
      r = self.grid_x/5
      pygame.draw.line(self.screen, farbe,(cx-r,cy-r),(cx+r,cy+r), 4)
      pygame.draw.line(self.screen, farbe,(cx+r,cy-r),(cx-r,cy+r), 4)
      cy = 3*self.grid_y/4
      farbe = pygame.Color(64,64,255)
      pg2d = [[cx-r,cy],[cx+r,cy-r],[cx+r,cy+r],[cx-r,cy]]
      pygame.draw.polygon(self.screen, farbe, pg2d, 0)

      farbe = pygame.Color(128,128,255)
      dx =  self.grid_x
      cx = self.grid_x/2
      cy = self.grid_y/2
      x = dx
      for i in range(len(self.store)):
         cx += dx
         pg2d = [[cx+2*r,cy],[cx-2*r,cy-r],[cx-2*r,cy+r],[cx+2*r,cy]]
         pygame.draw.polygon(self.screen, farbe, pg2d, 0)

      if self.T:
         self.PLOT_BUTTONS()

   def PLOT_BUTTONS(self):
      font = pygame.font.SysFont('arial',int(self.grid_y))
      for i in range(len(self.B)):
         b = self.B[i]
         plg = [b[0], [b[1][0],b[0][1]],b[1], [b[0][0],b[1][1]],b[0]]
         #pygame.draw.polygon(self.screen,(255,0,0),plg,0)
         pygame.draw.polygon(self.screen,(255,255,0),plg,2)
         text = font.render(self.Text[i],1,(255,255,0)) 
         self.screen.blit(text, (b[0][0]+10, b[0][1]+int(self.grid_y/3)))

   def CONTROL(self, mouse, button):
      PRINT ('CONTROL ', mouse)
      if ( self.grid_y < mouse[1] and mouse[1] < self.size_y-self.grid_y):
         return False
      if button[1] : return False

      if ( mouse[1] < self.grid_y) :
         if ( mouse[0] < self.grid_x ):
            if not self.record: # 
               self.record = True # start recoder 
               PRINT ('start Record')
               self.rs = len(self.steps)
            else:
               self.record = False # end record
               PRINT ('end Record')
               if ( self.steps[self.rs:]):
                  self.store.append(self.steps[self.rs:])
                  steps = copy.deepcopy(self.steps[self.rs:])
                  seiten = []
                  for step in steps:
                     if not step[0] in seiten:
                        seiten.append(step[0])
                        
                  if len(seiten) == 3:
                     for step in steps:
                        if step[0] == seiten[0]: step[0] = seiten[2]
                        elif step[0] == seiten[2]: step[0] = seiten[0]
                  for i in range(len(steps)):
                     steps[i][1] = -steps[i][1]
                  self.store.append(steps)

         elif (mouse[0] > self.size_x-self.grid_x):
            if ( mouse[1] < self.grid_y/2 ):
               self.CTRL_X()
            else:
               self.CTRL_Z()
         else:
            if button[0]:
               self.PLAY_STEPS(mouse[0])
            else:
               PRINT ('color edit')
         self.PLOT()
         return True

   def CTRL_Z(self):      
      if len(self.steps)>0 :
         step = self.steps.pop()
         step[1] *= -1
         self.ROTADE_SIDE(step)  
   
   def CTRL_X(self):      
      self.steps = []
      self.rubik.RESET()
      self.PLOT()

   def CTRL_C(self,mouse):
      i0,j0 = self.GET_PLG(mouse)
      self.strg_c = []
      PRINT('i0= ',i0,', j0= ',j0)
      ij = self.GET_NEIGHB(i0,j0)
      self.strg_c = ij
      PRINT('STRG_C ij= ',ij)
      self.PLOT()

   def CTRL_V(self,mouse):
      PRINT('STRG_V ', mouse)
      i0,j0 = self.GET_PLG(mouse)
      ij = self.GET_NEIGHB(i0,j0)
      PRINT('STRG_V ij ',ij)
      PRINT('STRG_V self.strg_c', self.strg_c)
      pg=self.rubik.GET_PLGS()
      if len(ij) == len(self.strg_c):
         for i in range(len(ij)):
            PRINT( 'ij[i], self.strg_c[i],i',ij[i], self.strg_c[i],i)
            if len(ij) == 2 or i == 0:
               tmp = pg[ij[i][0]][ij[i][1]]
               pg[ij[i][0]][ij[i][1]] = pg[self.strg_c[i][0]][self.strg_c[i][1]]
               pg[self.strg_c[i][0]][self.strg_c[i][1]] = tmp
            else:
               if ij[i][2] == self.strg_c[i][2] :
                  tmp = pg[ij[i][0]][ij[i][1]]
                  pg[ij[i][0]][ij[i][1]] = pg[self.strg_c[i][0]][self.strg_c[i][1]]
                  pg[self.strg_c[i][0]][self.strg_c[i][1]] = tmp
               else:
                  if i+1 < len(ij): i1=i+1
                  else: i1=i-1
                  tmp = pg[ij[i1][0]][ij[i1][1]]
                  pg[ij[i1][0]][ij[i1][1]] = pg[self.strg_c[i][0]][self.strg_c[i][1]]
                  pg[self.strg_c[i][0]][self.strg_c[i][1]] = tmp
      self.strg_c=[]
      self.PLOT()

   def GET_PLG(self,mouse):
      pg = self.rubik.GET_PLGS()
      for i in range(len(pg)):
         for j in range(len(pg[i])):
            if self.TO_PAINT(pg[i][j]) :
               pg2d = self.PLG2D(pg[i][j])   
               if self.IN_PLG(mouse, pg2d) :
                  PRINT('i= ',i,', j= ',j)
                  PRINT(pg[i][j])
                  return i, j        
      return -1, -1

   def GET_NEIGHB(self,i0,j0):
      pg = self.rubik.GET_PLGS()
      test_plg = pg[i0][j0]
      ij=[]
      ij.append([i0,j0])
      for i in range(len(pg)):
         #if i0 != i:
            for j in range(len(pg[i])-1): # Polygon in der Mitte weglassen
               for k in range(len(pg[i][j])-1):
                  for l in range(len(pg[i0][j0])-1):
                     diff = (pg[i][j][k]+pg[i][j][k+1])-(pg[i0][j0][l]+pg[i0][j0][l+1])
                     dist = np.inner(diff,diff)
                     if dist < 0.01 and j0%2 == j%2 and (i0 != i or j0 != j):
                        ij.append([i,j,k,l])
                        PRINT('dist= ', dist, 'ij ',ij)
      PRINT (ij)
      return ij

   def PLAY_STEPS(self, x=0):
      PRINT ('PLAY_STEPS ',x)
      stp = int(x/self.grid_x -1)
      angle = self.rubik.GET_ANGLE()
      if (len(self.store) > stp):
         for step in  self.store[stp]:
            self.ROTADE_SIDE(step)

   def CTRL_S(self):
      #Tk().withdraw()
      file_path_string = tkinter.filedialog.asksaveasfilename()
      try:
         with open(file_path_string, 'w') as f :
            json.dump([self.steps, self.store], f)
      except :
         PRINT ('File open failed')

   def CTRL_O(self):
      #Tk().withdraw()
      file_path_string = tkinter.filedialog.askopenfilename()
      try:
         with open(file_path_string, 'r') as f :
            self.steps, self.store = json.load(f)
      except :
         PRINT ('File open failed')
      PRINT (self.store)
      for step in  self.steps:
         self.ROTADE_SIDE(step)
      self.PLOT()   

   def RANDOM(self, n):
      step =[0,0] 
      for i in range(int(n)+2):
         step[0] = random.randint(0, 11)
         step[1] = random.randint(0, 1)*2 -1
         self.ROTADE_SIDE(step)
      return False

   def HELP(self):
      PRINT('HELP')
      line = 500
      font = pygame.font.SysFont('arial',18)
      text = font.render('Dodekaeder Hilfe (F1)',1,(255,255,255))
      self.screen.blit(text, (50, line))
      font = pygame.font.SysFont('arial',14)
      texte = ['MMB oder SHIFT, rotieren'] 
      #texte += ['mit SHIFT kann Rot-Achse geklemmt werden']
      texte += ['LMB Rubik Seide links drehen']
      texte += ['RMB Rubik Seide rechts drehen']
      texte += ['Druecken von roten Button links oben Zugfolge aufzeichnen starten, erneutes druecken benden']
      texte += ['STRG+s, Aufzeichnung speichern']
      texte += ['STRG+o, Aufzeichnung einlesen']
      texte += ['Blaue Pfeile Zugfolge anwenden']
      texte += ['STG+z oder blauer Pfeil oben rechts 1 Zug zurueck']
      texte += ['STG+x oder rotes Kreuz oben rechts Reset']
      texte += ['STG+..eine beliebige Ziffer n, n+2 zufällige Zuege']
      texte += ['STG+c / STRG+v , copy paste von Teilen']
      for tt in texte:
         line += 20
         text = font.render(tt,1,(255,255,255))
         self.screen.blit(text, (50, line))
