# -*- coding: UTF-8 -*- 

# Import modules 
import json
import copy
from tkinter import *
import tkinter.filedialog
import re
import pygame 
import pygame.freetype
from pygame.locals import * 
import sys
import optparse
import math as M
import random
import numpy as np
from Dodekaeder import Dodekaeder

class Game():
   def INIT(S, sc, rubik):
      S.mouse_pressed=False
      S.mouse_moved=False
      S.shift=False
      S.rot_alpha=0
      S.do_rot_side=0
      S.rubik = rubik
      S.strg = False
      S.steps =[]
      S.text = []
      S.record = 0
      S.store = []
      S.rs = -1

      S.farben = []
      S.farben.append(pygame.Color(128,0,0))
      S.farben.append(pygame.Color(255,255,0))
      S.farben.append(pygame.Color(0,0,127))
      S.farben.append(pygame.Color(0,64,0))
      S.farben.append(pygame.Color(128,0  ,127))
      S.farben.append(pygame.Color(64,64,64))

      S.farben.append(pygame.Color(64,127,255))
      S.farben.append(pygame.Color(255,255,255))
      S.farben.append(pygame.Color(64,255,64))
      S.farben.append(pygame.Color(255,127,127))
      S.farben.append(pygame.Color(0,128,0))
      S.farben.append(pygame.Color(255,127,0))

      
      S.screen = sc
      S.size_x = S.screen.get_width()
      S.size_y = S.screen.get_height()
      S.mid = [float(S.size_x)/2.0, float(S.size_y)/2.0 ]
      S.size = float(min(S.size_x, S.size_y))
      S.scale = 0.15*S.size
      S.grid_x =  40 #S.size_x/20
      S.grid_y =  40 #S.size_y/20

      S.status_line = pygame.Surface((S.size_x, S.size_y/S.grid_y))

      S.mat = np.zeros((3,3), np.float)
      S.mat[0][0] = S.mat[1][1] = S.mat[2][2]= 1.0
      S.scl = S.mat
      S.mat_last = S.mat
      S.alpha = 0.0
      S.beta = 0.0
      S.gamma = 0.0
      S.delta = 6
      S.help = False

   def GRID_X(S): return S.grid_x
   def GRID_Y(S): return S.grid_y
   
   def SAVE(S):
      Tk().withdraw()
      file_path_string = tkinter.filedialog.asksaveasfilename()
      try:
         with open(file_path_string, 'w') as f :
            json.dump([S.steps, S.store], f)
      except :
         print ('File open failed')


   def READ(S):
      Tk().withdraw()
      file_path_string = tkinter.filedialog.askopenfilename()
      try:
         with open(file_path_string, 'r') as f :
            S.steps, S.store = json.load(f)
      except :
         print ('File open failed')
      S.PLOT()   
      return

   def RANDOM(S, n):
      step =[0,0] 
      for i in range(n):
         step[0] = random.randint(0, 11)
         step[1] = random.randint(0, 1)*2 -1
         S.ROTADE_SIDE(step)
     

   def SET_STATUS_MP(S,mp):
      if S.mouse_pressed != mp:
         S.mouse_pressed=mp
         S.do_rot_side=S.strg
      S.mouse_moved=False
      S.mat_last = S.mat
      S.alpha = 0.0
      S.beta = 0.0
      S.gamma = 0.0
   def SET_STATUS_SHIFT(S,shift):
      S.shift=shift
      S.rot_alpha=0
   def SET_STATUS_STRG(S,strg):
      S.strg = strg
   def STRG_Z(S):
      if len(S.steps):
         angle = S.rubik.get_angle()
         step = S.steps.pop()
         step[1] = -step[1]
         S.ROTADE_SIDE(step)
   def STRG_X(S):
      S.steps = []
      S.rubik.reset()

   def ROTADE_SIDE(S, step):
      print ('ROTADE_SIDE')
      delta = S.delta
      angle = S.rubik.get_angle()
      da = angle/delta
      for i in range(delta):
         S.rubik.rotate_side(step[0],step[1],da)
         S.PLOT()

   def MOUSE_MOVE(S, mouse, mouse_move):
      if not S.mouse_moved and (mouse_move[0] or mouse_move[1] ):
         S.mouse_moved = True
         
      if S.mouse_moved:
         if S.strg and S.mouse_pressed:
            if S.do_rot_side:
               S.do_rot_side = False
               print ( 'do_rot_side')
               if S.GET_SIDE(mouse, mouse_move):
                  step = S.steps[len(S.steps)-1]
                  S.ROTADE_SIDE(step)
         else:
            dx = mouse[0] -S.mid[0]
            dy = mouse[1] -S.mid[1]
            if dx*dx + dy*dy > 200*200 and S.rot_alpha == 0:
               S.rot_alpha = 3
               S.ROT(mouse, mouse_move)
               S.rot_alpha = 0
            else:
               if not S.rot_alpha and S.shift:
                  if mouse_move[0]*mouse_move[0] > mouse_move[1]*mouse_move[1]:
                     S.rot_alpha = 1
                  elif mouse_move[0]*mouse_move[0] < mouse_move[1]*mouse_move[1]:
                     S.rot_alpha = 2
               S.ROT(mouse, mouse_move)
      return

   def ROT(S,mouse, mv):
      if S.rot_alpha == 0 or S.rot_alpha == 1:
         S.alpha = S.alpha+2.0*float(mv[0])/S.size_x*M.pi
      if S.rot_alpha == 0 or S.rot_alpha == 2:
         S.beta  = S.beta+2.0*float(mv[1])/S.size_y*M.pi
      if S.rot_alpha == 3 :
         delta  = 2.0*M.sqrt(float(mv[1]*mv[1]+mv[0]*mv[0]))/S.size_y*M.pi
         if ( (mouse[0]-S.mid[0])*mv[1] - (mouse[1]-S.mid[1])*mv[0] ) > 0:
            delta = -delta
         S.gamma +=delta   
      rot_x = np.zeros((3,3), np.float)
      rot_x[1][1]= rot_x[2][2]=M.cos(S.beta)
      rot_x[1][2]=M.sin(S.beta)
      rot_x[2][1]= -rot_x[1][2]
      rot_x[0][0]= 1.0

      rot_y = np.zeros((3,3), np.float)
      rot_y[1][1]= 1.0
      rot_y[0][0]= rot_y[2][2]=M.cos(S.alpha)
      rot_y[0][2]=M.sin(S.alpha)
      rot_y[2][0]= -rot_y[0][2]

      rot_z = np.zeros((3,3), np.float)
      rot_z[2][2]= 1.0
      rot_z[0][0]= rot_z[1][1]=M.cos(S.gamma)
      rot_z[0][1]=M.sin(S.gamma)
      rot_z[1][0]= -rot_z[0][1]
      S.mat = rot_x.dot(rot_y.dot(rot_z.dot(S.mat_last))) 
      return

   def GET_SIDE(S,mouse,mouse_move):
      #print ( mouse, mouse_move)
      centers,plgs = S.rubik.get_side_plgs()
      i=-1
      for plg3d in plgs:
         i += 1
         if ( S.TO_PAINT(plg3d)):
            pg2d = S.PLG2D(plg3d)
            if S.IN_PLG(mouse,pg2d) : 
               center2d = S.PT2D(centers[i])
               sign = (mouse[1]-center2d[1])*mouse_move[0] - (mouse[0]-center2d[0])*mouse_move[1]
               if sign > 0 : sign = -1
               elif sign < 0 : sign = 1
               S.steps.append([i, sign])
               return True
      return False

   def TO_PAINT(S, plg):
      v1 = plg[1]-plg[0]
      v2 = plg[2]-plg[1]
      v3 = np.zeros(3, np.float)
      v3 = ((v1[1]*v2[2] - v1[2]*v2[1]), (v1[2]*v2[0] - v1[0]*v2[2]), (v1[0]*v2[1] - v1[1]*v2[0]))
      v1 = S.mat.dot( plg[1])   
      v3 = S.mat.dot(v3)
      if v1.dot(v3) >0 :
         # print ('+')
         return v3[2] >0
      else:
         # print ('-')
         return v3[2] <0

   def PLG2D(S,plg3d):
      pg2d = []
      for pt in plg3d:
         PT2D = S.PT2D(pt)
         pg2d.append( PT2D ) 
      return pg2d

   def PT2D(S,pt3d):
      pt3d = S.mat.dot(pt3d)
      pt = [int( S.mid[0]+pt3d[0]*S.scale),int(S.mid[1]+pt3d[1]*S.scale)]
      return pt

   def PLG2D(S,plg3d):
      pg2d = []
      for pt in plg3d:
         PT2D = S.PT2D(pt)
         pg2d.append( PT2D ) 
      return pg2d

   def IN_PLG(S,m,pg2d):
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

   def PLOT(S):
      S.screen.fill((0,20,60))
      plgs = S.rubik.get_plgs()
      centers = S.rubik.get_centers()
      for i in range(0,len(plgs)):
         S.PLOT_PG(plgs,centers[i])
      S.PLOT_STEPS()
      S.PLOT_STATUS()
      S.PLOT_TEXT()
      S.PLOT_CIRCLE()
      pygame.display.flip()

   def PLOT_CIRCLE(S):
      x = S.size_x/2 -5.5*S.grid_x
      y = S.size_y - S.grid_x/2

      radius = S.grid_y/3
      for i in range(0,12):
         center = (x,y)
         pygame.draw.circle(S.screen, S.farben[i], center, radius)
         x += S.grid_y

   def PLOT_STATUS(S):
      c = (S.grid_x/2, S.grid_y/2)
      r = S.grid_x/3
      frb1 = pygame.Color(255,0,0)
      frb2 = pygame.Color(128,0,0)
      frb3 = pygame.Color(192,0,0)
      if ( S.record == True) :
         f1 = frb1
         f2 = frb2
      else:
         f2 = frb1
         f1 = frb2

      pg2d = [[c[0]-r,c[1]+r],[c[0]-r,c[1]-r],[c[0]+r,c[1]-r],[c[0]+r,c[1]+r]]
      pygame.draw.polygon(S.screen, frb3, pg2d, 0)
      pygame.draw.lines(S.screen, f2, False, pg2d[:3], 4)
      pg2d = [[c[0]-r,c[1]+r],[c[0]+r,c[1]+r],[c[0]+r,c[1]-r],[c[0]-r,c[1]-r]]
      pygame.draw.lines(S.screen, f1, False, pg2d[:3], 4)

      farbe = pygame.Color(255,0,0)
      cx = S.size_x-S.grid_x/2
      cy = S.grid_y/4
      r = S.grid_x/5
      pygame.draw.line(S.screen, farbe,(cx-r,cy-r),(cx+r,cy+r), 4)
      pygame.draw.line(S.screen, farbe,(cx+r,cy-r),(cx-r,cy+r), 4)
      cy = 3*S.grid_y/4
      farbe = pygame.Color(64,64,255)
      pg2d = [[cx-r,cy],[cx+r,cy-r],[cx+r,cy+r],[cx-r,cy]]
      pygame.draw.polygon(S.screen, farbe, pg2d, 0)

      farbe = pygame.Color(128,128,255)
      dx =  S.grid_x
      cx = S.grid_x/2
      cy = S.grid_y/2
      x = dx
      for i in range(len(S.store)):
         cx += dx
         pg2d = [[cx+2*r,cy],[cx-2*r,cy-r],[cx-2*r,cy+r],[cx+2*r,cy]]
         pygame.draw.polygon(S.screen, farbe, pg2d, 0)


   def PLOT_PG(S, pg, normal):
      schwarz = pygame.Color(0,0,0)
      normal = S.mat.dot(normal)
      #if normal[0] > 0 :
      if True :
         i=0
         for plgs in pg:
            color = S.farben[i]
            i +=1
            for plg3d in plgs:
               if S.TO_PAINT(plg3d) :
                  pg2d = S.PLG2D(plg3d)   
                  pygame.draw.polygon(S.screen, color, pg2d, 0)
                  pygame.draw.polygon(S.screen, schwarz, pg2d, 4)
      
   def PLOT_STEPS(S):
      dx =  S.grid_x
      x = 2*dx
      S.plot_steps(S.steps, S.size_x)
      if S.record : S.plot_steps(S.steps[S.rs:], dx)
      for  steps in S.store:
         S.plot_steps(steps, x)
         x += dx
   def plot_steps(S, steps, x):
      dx = S.grid_x/2
      dy = S.grid_y/2
      xl = x -1.0*dx
      xr = x -0.5*dx
      ys = S.grid_y
      r = 0.4*dy
      nmin= max(len(steps)-35,0)
      nmax= max(len(steps),0)
      stps = steps[nmin:nmax]
   
      for step in stps:
         if step[1] == -1: x=xl
         else: x=xr
         ys +=dy
         center = (x, ys)
         pygame.draw.circle(S.screen, S.farben[step[0]], center, r)

   def CONTROL(S, mouse, button):
      print ('CONTROL ', mouse)
      if ( mouse[1] > S.grid_y and mouse[1] < S.size_y-S.grid_y):
         return False
      if button[1] : return false

      if ( mouse[1] < S.grid_y) :
         if ( mouse[0] < S.grid_x ):
            if not S.record: # 
               S.record = True # start recoder 
               print ('start Record')
               S.rs = len(S.steps)
            else:
               S.record = False # end record
               print ('end Record')
               if ( S.steps[S.rs:]):
                  S.store.append(S.steps[S.rs:])
                  steps = copy.deepcopy(S.steps[S.rs:])
                  re = len(S.steps)
                  S.steps = S.steps + steps
                  ree = len(S.steps)
                  for i in range(re,ree):
                     S.steps[i][1] = -S.steps[i][1]
                  S.store.append(S.steps[re:])

         elif (mouse[0] > S.size_x-S.grid_x):
            if ( mouse[1] < S.grid_y/2 ):
               #reset
               S.STRG_X()
            else:
               S.STRG_Z()
         else:
            if button[0]:
               S.PLAY_STEPS(mouse[0])
            else:
               print ('color edit')
         S.PLOT()
         return True
      else:
         x = S.size_x/2 -6*S.grid_x
         i = int((mouse[0]-x)/S.grid_x)
         if button[0] == 0: sign =1
         else: sign = -1
         S.steps.append([i, sign])
         delta = S.delta
         angle = S.rubik.get_angle()
         da = angle/delta
         if i<12:
            for k in range(delta):
               S.rubik.rotate_side(i,sign,da)
               S.PLOT()
         return True
      return False

   def PLAY_STEPS(S, x=0):
      print ('PLAY_STEPS ',x)
      stp = int(x/S.grid_x -1)
      angle = S.rubik.get_angle()
      delta = S.delta
      S.delta = 3
      if (len(S.store) > stp):
         for step in  S.store[stp]:
            #S.rubik.rotate_side(step[0],step[1],angle)
            S.ROTADE_SIDE(step)
      S.delta = delta

   def HELP(S, val):
      S.help = val
      print ('S.help', S.help)
   def PLOT_TEXT(S):
      #2Font =  pygame.freetype.Font(None, 20)
      if S.help:
         line = 25
         font = pygame.font.SysFont('arial',18)
         text = font.render('Dodekaeder Hilfe',1,(255,255,255))
         S.screen.blit(text, (50, line))
         font = pygame.font.SysFont('arial',14)
         line += 20
         text = font.render('Linke Maustaste gedrückt Rotieren',1,(255,255,255))
         S.screen.blit(text, (50, line))
         line += 20
         text = font.render('mit größer kann Rot-Achse geklemmt werden',1,(255,255,255))
         S.screen.blit(text, (50, line))
         line += 20

def RubikDodekaeder():

   pygame.init()
   size_x=1200
   size_y=800
   screensize = (size_x,size_y)
   screen = pygame.display.set_mode(screensize)
   game = Game()
   rubik = Dodekaeder()
   rubik.init()
   game.INIT(screen,rubik)

   game.PLOT()

   #pygame.display.flip()

   mouse_pressed = False
   aufzeichnung =False

   while True:
      event = pygame.event.wait()##.type == KEYDOWN or MOUSEBUTTONDOWN or QUIT
      if event.type == QUIT:
         pygame.quit()
         return

      mouse = pygame.mouse.get_pos()
      mouse_move = pygame.mouse.get_rel()
      button_pressed = pygame.mouse.get_pressed()

      if event.type == 1025: # Button pressed
         mouse_pressed = True
         game.SET_STATUS_MP(mouse_pressed)
         print ("mouse button pressed")
         if game.CONTROL(mouse, button_pressed):
            continue
      if event.type == 1026: # Button released
         mouse_pressed = False
         game.SET_STATUS_MP(mouse_pressed)
         print ("mouse button released")
         continue
      if event.type == 768: # Key pressed
         print ("Key pressed")
         print (pygame.key.get_mods())
         taste = pygame.key.name(event.key)
         print (taste)
         if taste == 'f1' : #r
            game.HELP(True)
            game.PLOT()
            game.HELP(False)
            print ('Hilfe Text')
         if pygame.key.get_mods() & pygame.KMOD_SHIFT: 
            print ("shift pressed")
            game.SET_STATUS_SHIFT(True)
         if pygame.key.get_mods()  & pygame.KMOD_CTRL: 
            print ("strg pressed")
            print (event.key)
            game.SET_STATUS_STRG(True)
            if taste == 'x':
               game.STRG_X()
               game.PLOT()
            elif taste == 'z':
               game.STRG_Z()
               game.PLOT()
            elif taste == 's' : #s
               print ('SAVE_STEPS')
               game.SAVE()
            elif taste == 'r' : #r
               print ('Read Session')
               game.READ()
            elif 49 <= event.key and event.key <= 57 : #ziffer 1-9
               print ('RANDOM')
               game.RANDOM( event.key-47 )

      if event.type == 769: # Key released
         print ("Key released")
         print (pygame.key.get_mods())
         print (event.type)
         taste = pygame.key.name(event.key)
         print (taste)
         print ("shift released")
         game.SET_STATUS_SHIFT(False)
         game.SET_STATUS_STRG(False)

      if button_pressed[0] or button_pressed[1] or button_pressed[2]:
         game.MOUSE_MOVE(mouse, mouse_move)
         game.PLOT()

if __name__ == "__main__":

   parser = optparse.OptionParser(usage="usage: %prog  ")
   (options, args) = parser.parse_args()

   print('*********************** **')
   print('*  options     *')
   print(options, args)
   
   RubikDodekaeder()
