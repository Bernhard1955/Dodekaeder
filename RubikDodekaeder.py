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
from eventhandling import Eventhandling
from Dodekaeder import Dodekaeder


def RubikDodekaeder(verbose):


   pygame.init()
   size_x=1200
   size_y=800
   screensize = (size_x,size_y)
   screen = pygame.display.set_mode(screensize)
   game = Eventhandling()
   rubik = Dodekaeder()
   rubik.INIT()
   game.INIT(screen,rubik,verbose)


   game.HELP(True)
   game.PLOT()
   game.HELP(False)

   #pygame.display.flip()

   mouse_pressed = False
   aufzeichnung =False
   V = verbose

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
         if V: print ("mouse button pressed")
         if game.CONTROL(mouse, button_pressed):
            continue
      if event.type == 1026: # Button released
         mouse_pressed = False
         game.SET_STATUS_MP(mouse_pressed)
         if V: print ("mouse button released")
         continue
      if event.type == 768: # Key pressed
         if V: print ("Key pressed")
         if V: print (pygame.key.get_mods())
         taste = pygame.key.name(event.key)
         if V: print (taste)
         if taste == 'f1' : #r
            game.HELP(True)
            game.PLOT()
            game.HELP(False)
            if V: print ('Hilfe Text')
         if pygame.key.get_mods() & pygame.KMOD_SHIFT: 
            if V: print ("shift pressed")
            game.SET_STATUS_SHIFT(True)
         if pygame.key.get_mods()  & pygame.KMOD_CTRL: 
            if V: print ("strg pressed")
            if V: print (event.key)
            game.SET_STATUS_STRG(True)
            if taste == 'c':
               game.STRG_C(mouse)
               game.PLOT()
            if taste == 'v':
               game.STRG_V(mouse)
               game.PLOT()
            if taste == 'x':
               game.STRG_X()
               game.PLOT()
            elif taste == 'z':
               game.STRG_Z()
               game.PLOT()
            elif taste == 's' : #s
               if V: print ('SAVE_STEPS')
               game.SAVE()
            elif taste == 'o' : #r
               if V: print ('Read Session')
               game.READ()
            elif 49 <= event.key and event.key <= 57 : #ziffer 1-9
               if V: print ('RANDOM')
               game.RANDOM( event.key-47 )

      if event.type == 769: # Key released
         if V: print ("Key released")
         if V: print (pygame.key.get_mods())
         if V: print (event.type)
         taste = pygame.key.name(event.key)
         if V: print (taste)
         if V: print ("shift released")
         game.SET_STATUS_SHIFT(False)
         game.SET_STATUS_STRG(False)

      if button_pressed[0] or button_pressed[1] or button_pressed[2]:
         game.MOUSE_MOVE(mouse, mouse_move)
         game.PLOT()

if __name__ == "__main__":

   parser = optparse.OptionParser(usage="usage: %prog  ")
   parser.add_option(
      "-v", action="store_true", dest="verbose", default=False, help="verbose mode, default = False")
   (options, args) = parser.parse_args()


   verbose = options.verbose
   print(options, args)
   
   RubikDodekaeder( verbose)
