# Import modules 
import optparse
from eventhandling import Eventhandling
from Geometry import Geometry

def RubikDodekaeder(verbose, cubic):

   if cubic:
      rubik = Geometry()
   else:
      rubik = Geometry('Dodekaeder')
      
   EV = Eventhandling(rubik,verbose)

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
