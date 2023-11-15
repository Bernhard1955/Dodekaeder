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
from Geometry import Geometry


def RubikDodekaeder(verbose, cubic):

   pygame.init()
   size_x=1200
   size_y=800
   screensize = (size_x,size_y)
   screen = pygame.display.set_mode(screensize)
   if cubic:
      rubik = Geometry()
   else:
      rubik = Geometry('Dodekaeder')
      
   EV = Eventhandling(screen,rubik,verbose)
   EV.PLOT()

   #pygame.display.flip()

   mouse_pressed = False
   aufzeichnung =False
   V = verbose

   while True:
      EV.WAIT()
      return

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
