__author__ = 'Kunxuan'

import os.path
import sys
import math
from scipy.integrate import quad
from scipy.special import gamma

# las2txt -i "file" -parse xyznca
class LAD:
    """
    takes txt file of tree points, return LAD distribution
    to get lad for a voxel, init with ref file to set voxel limits, run setLAD with desired file to set LAD
    """

    def __init__(self, filename, vNum):
        # set by processFile
        # self.file = 0
        self.points = []

        # set by setVoxel
        self.vSet = 0
        self.limits = [999, -999] # min, max
        self.vNum = vNum
        self.h = 0
        self.heights = []

        # var change with each file
        self.voxCount = [0]*self.vNum
        self.vegCount = [0]*self.vNum
        self.diSum_vox = [0]*self.vNum
        self.diSum_veg = [0]*self.vNum
        self.dgSum = [0]*self.vNum
        self.groundCount = 0
        self.lad = [0]*self.vNum
        self.lai = 0

        self._processFile(filename)
        self._setVoxel()

    def _resetLAD(self):
        # var change with each file
        self.voxCount = [0]*self.vNum
        self.vegCount = [0]*self.vNum
        self.diSum_vox = [0]*self.vNum
        self.diSum_veg = [0]*self.vNum
        self.dgSum = [0]*self.vNum
        self.groundCount = 0
        self.lad = [0]*self.vNum
        self.lai = 0

    def _processFile(self, filename):
        if not os.path.isfile(filename):
            print("File " + filename + " does not exist")
            sys.exit(1)

        # try to open file
        try:
            # print "reading file ", filename
            # self.file = os.open(filename, os.O_RDONLY | os.O_NONBLOCK)
            file = open(filename, "rb")
        except:
            print("Could not open file")
            sys.exit(1)

        self.points = []

        for line in file:
            pt = self.readline(line)
            self.points.append(pt)

    def _setVoxel(self):
        # set voxel limits given using reference file
        if self.vSet:
            print "resetting voxel?..."
        else:
            print "setting voxel"
        self.vSet = 1

        for pt in self.points:
            # check min/max
            z = pt[2]
            if z<self.limits[0]:
                self.limits[0] = z
            elif z>self.limits[1]:
                self.limits[1] = z

        # get voxel limits
        self.h = (self.limits[1] - self.limits[0])/self.vNum
        for i in range(1, self.vNum):
            self.limits.insert(i, self.limits[0]+self.h*i)

        # get heights
        for i in range(0, self.vNum):
            self.heights.append((self.limits[i] + self.limits[i+1])/2-self.limits[0])


    def setLAD(self, filename, newFile):
        if newFile:
            # print "processing new file..."
            self._processFile(filename)

        if not self.vSet:
            print "voxel limits not set, calling setVoxel with current file..."
            self._setVoxel()

        self._resetLAD()
        # total each voxel
        # np.histogram?
        for pt in self.points:
            for i in range(0, self.vNum):
                if self.limits[i] <= pt[2] <= self.limits[i+1]:
                    self.voxCount[i] += 1/pt[3]
                    self.diSum_vox[i] += (self.limits[i+1]-pt[2])/math.cos(math.radians(pt[5]))
                    # classification
                    if pt[4] in [3, 4, 5]:
                        self.vegCount[i] += 1/pt[3]
                        self.diSum_veg[i] += (self.limits[i+1]-pt[2])/math.cos(math.radians(pt[5]))
                    # add to dg of all voxels above it
                    for j in range(i+1, self.vNum):
                        self.dgSum[j] += self.h/math.cos(math.radians(pt[5]))
                    break
            else:
                print 'problem point: ', pt, ' z limits: ', self.limits[0], self.limits[self.vNum]

        # print self.voxCount
        # print self.vegCount

        # get lad
        Ng = 0
        dg = 0
        for i in range(0,self.vNum):
            Ni = self.vegCount[i]
            # avg distance 0f Ni beams
            # print self.diSum_veg[i], self.vegCount[i]
            di = 0 if self.diSum_veg[i] == 0 else self.diSum_veg[i]/self.vegCount[i]
            Ng_temp = Ng + (self.voxCount[i] - Ni)
            dg_temp = self.dgSum[i] + (self.diSum_vox[i]-self.diSum_veg[i])
            dg = 0 if Ng_temp == 0 else dg_temp/Ng_temp #dg_temp = 0 ?
            div = (Ni*di+Ng_temp*dg)
            if div == 0:
                self.lad[i] = 0
            else:
                self.lad[i] = Ni/div/0.5  # G function = 0.5
            Ng += self.voxCount[i]

        # self.pt_lad()

        # for i in range(0, self.vNum):
        #     self.lai += self.heights[i]*self.lad[i]*h
        self.lai = sum(self.lad)*self.h
        # print self.lai

        # print 'Heights'
        # for i in reversed(self.heights): print i
        # print 'LAD'
        # for i in reversed(self.lad): print i

    def readline(self, line):
        return tuple([float(i) for i in line.split(" ")])

    def pt_lad(self):
        for i in range(1, self.vNum+1):
            print self.heights[-1*i], ", ", self.lad[-1*i]

    def pt_lad(self, lad):
        for i in range(1, self.vNum+1):
            print self.heights[-1*i], ", ", lad[-1*i]

def G_integrand(x, th):
    # A function
    test = 1/math.tan(th)/math.tan(x)
    A = 0
    if abs(test) >= 1:
        A = math.cos(th)*math.cos(x)
    else:
        y = math.acos(test)
        A = math.cos(th)*math.cos(x)*(1+2/math.pi*(math.tan(y)-y))

    # LADF  Beta Distribution method
    u = 0
    v = 0
    B = gamma(u)*gamma(v)/gamma(u+v)
    t = 2*x/math.pi
    f = math.pow((1-t), (u-1))*math.pow(t, (v-1))/B
    return A*f

def G_fun(a):
    G = quad(G_integrand, 0, math.pi/2, args=a)
    return G

