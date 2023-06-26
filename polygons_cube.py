import numpy as np

def polygons():
   dkz = np.zeros((6,1,5,3),np.float64)
   dk  = np.zeros((6,8,5,3),np.float64)
   rot_x = np.zeros((3,3), np.float64)
   rot_y = np.zeros((3,3), np.float64)
   rot_z = np.zeros((3,3), np.float64)
   rot_x[0][0]  = rot_x[2][1] = 1.0
   rot_x[1][2] -= rot_x[2][1]
   rot_y[1][1]  = rot_y[2][0] = 1.0
   rot_y[0][2] -= rot_y[2][0]
   rot_z[1][0]  = rot_z[2][2] = 1.0
   rot_z[0][1] -= rot_z[1][0]

# NEW_MOLECULE
# POLYG
# 6
   dkz[ 0][0][0]=( 20.0, 20.0, 60.0)
   dkz[ 0][0][1]=(-20.0, 20.0, 60.0)
   dkz[ 0][0][2]=(-20.0,-20.0, 60.0)
   dkz[ 0][0][3]=( 20.0,-20.0, 60.0)
   dkz[ 0][0][4]=( 20.0, 20.0, 60.0)

   trans_x = np.array([40.0,  0.0, 0.0])
   trans_y = np.array([ 0.0, 40.0, 0.0])
   for i in range(0,len(dkz[0][0])):
      dk[0][0][i] = dkz[0][0][i] + trans_y

   for i in range(0,len(dkz[0][0])):
      dk[0][1][i] = dk[0][0][i] + trans_x

   for i in range(1,4):
      dk[0][2*i  ] = dk[0][(i-1)*2  ].dot(rot_z)
      dk[0][2*i+1] = dk[0][(i-1)*2+1].dot(rot_z)

   for i in range(1,4):
      dk[i] = dk[i-1].dot(rot_y)
      dkz[i] = dkz[i-1].dot(rot_y)
   dk[4] = dk[1].dot(rot_z)
   dkz[4] = dkz[1].dot(rot_z)
   dk[5] = dk[3].dot(rot_z)
   dkz[5] = dkz[3].dot(rot_z)     

   mid = np.zeros((6,3),np.float64)
   for i in range(0,len(dkz)):
      for j in range(0,len(dkz[i][0])-1):
         mid[i]+=dkz[i][0][j]
      mid[i] *=1/(len(dkz[i][0])-1)            

   dka = np.zeros((6,1,5,3),np.float64)
   for i in range(0,len(dkz)):
      for j in range(0,len(dkz[i][0])):
         dka[i][0][j] = mid[i]+ 2.3*(dkz[i][0][j]-mid[i])
   return dkz, dk, mid, dka
#
def CENTERS():
   dkz, dk, mid, dka = polygons()
   return mid
#
def SIDE_PLGS():
   dkz, dk, mid, dka = polygons()
   plgs =[]
   for plg in dka:
      plgs.append(plg[0])
   return plgs
#
def PLGS():
   dkz, dk, mid, dka = polygons()
   sides =[]
   for i in range(0,len(dk)):
      pgs = []
      for pg in dk[i]:
         pgs.append(pg)
      pgs.append(dkz[i][0])
      sides.append(pgs)
   return sides
