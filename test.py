# Import modules 
import json
import tkinter.filedialog
import pygame 
from pygame.locals import * 
import sys
import optparse
import math as M
import random
from eventhandling import Eventhandling
from Dodekaeder import Dodekaeder
from Cube import Geometry


def RubikDodekaeder(verbose, cubic):

   pygame.init()
   size_x=1200
   size_y=800
   screensize = (size_x,size_y)
   screen = pygame.display.set_mode(screensize)
   EV = Eventhandling()
   if cubic:
      rubik = Geometry()
   else:
      rubik = Dodekaeder()
      
   rubik.INIT()
   EV.INIT(screen,rubik,verbose)


   EV.HELP(True)
   EV.PLOT()
   EV.HELP(False)

   #pygame.display.flip()

   mouse_pressed = False
   aufzeichnung =False
   V = verbose

   while True:
      event = pygame.event.wait()
      if event.type == QUIT:
         pygame.quit()
         return

      mouse = pygame.mouse.get_pos()
      mouse_move = pygame.mouse.get_rel()
      button_pressed = pygame.mouse.get_pressed()
      print ('button pressed', button_pressed)

      if event.type == 1025: # Button pressed
         mouse_pressed = True
         EV.SET_STATUS_MP(mouse_pressed)
         if V: print ("mouse button pressed")
         if EV.CONTROL(mouse, button_pressed):
            continue
      if event.type == 1026: # Button released
         mouse_pressed = False
         EV.SET_STATUS_MP(mouse_pressed)
         if V: print ("mouse button released")
         continue
      if event.type == 768: # Key pressed
         if V: print ("Key pressed")
         if V: print (pygame.key.get_mods())
         taste = pygame.key.name(event.key)
         if V: print (taste)
         if taste == 'f1' : #r
            EV.HELP(True)
            EV.PLOT()
            EV.HELP(False)
            if V: print ('Hilfe Text')
         if pygame.key.get_mods() & pygame.KMOD_SHIFT: 
            if V: print ("shift pressed")
            EV.SET_STATUS_SHIFT(True)
         if pygame.key.get_mods()  & pygame.KMOD_CTRL: 
            if V: print ("strg pressed")
            if V: print (event.key)
            EV.SET_STATUS_STRG(True)
            if taste == 'c':
               EV.STRG_C(mouse)
               EV.PLOT()
            if taste == 'v':
               EV.STRG_V(mouse)
               EV.PLOT()
            if taste == 'x':
               EV.STRG_X()
               EV.PLOT()
            elif taste == 'z':
               EV.STRG_Z()
               EV.PLOT()
            elif taste == 's' : #s
               if V: print ('SAVE_STEPS')
               EV.SAVE()
            elif taste == 'o' : #r
               if V: print ('Read Session')
               EV.READ()
            elif 49 <= event.key and event.key <= 57 : #ziffer 1-9
               if V: print ('RANDOM')
               EV.RANDOM( event.key-47 )

      if event.type == 769: # Key released
         if V: print ("Key released")
         if V: print (pygame.key.get_mods())
         if V: print (event.type)
         taste = pygame.key.name(event.key)
         if V: print (taste)
         if V: print ("shift released")
         EV.SET_STATUS_SHIFT(False)
         EV.SET_STATUS_STRG(False)

      if button_pressed[0] or button_pressed[1] or button_pressed[2]:
         EV.MOUSE_MOVE(mouse, mouse_move, button_pressed)
         EV.PLOT()

if __name__ == "__main__":

   parser = optparse.OptionParser(usage="usage: %prog  ")
   parser.add_option(
      "-v", action="store_true", dest="verbose", default=False, help="verbose mode, default = False")
   parser.add_option(
      "-q", action="store_true", dest="cubic", default=False, help="Play Rubik Cube, default = False")
   (options, args) = parser.parse_args()


   verbose = options.verbose
   cubic = options.cubic
   print(options, args)
   
   RubikDodekaeder( verbose, cubic)
