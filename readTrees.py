__author__ = 'Kunxuan'

import os.path
import sys
import LAD
import subprocess
import math

class readTrees:
    """
    takes list of tree locations, and classified LAS block
    extract trees, read LAD for each tree, pickle object
    """

    def __init__(self, treeFilename, lasFilename, FID_list):
        if not os.path.isfile(treeFilename):
            print("File " + treeFilename + " does not exist")
            sys.exit(1)

        # try to open file
        try:
            # print "reading file ", treeFilename
            # self.file = os.open(filename, os.O_RDONLY | os.O_NONBLOCK)
            self.treeFile = open(treeFilename, "rb")
        except:
            print("Could not open file")
            sys.exit(1)

        self.vNum = 8
        self.FID_list = FID_list
        self.LAD_list = []  #tuple of (FID, x, y, r, t, LAD_actual)
        self.LAD_cyn_list = []
        self.LAD_diff = []  #list of list at diff heights
        for i in range(0, self.vNum):
            self.LAD_diff.append([])
        self.defInName = lasFilename
        self.defOutName = r"C:\School\14au\Research\CZOSangamonIR\data_products\\"
        self.LAI_list = []
        self.LAI_cyn_list = []
        #self.extractTrees()
        # self.buildLists()

    # read with LAD
    def buildLists(self):
        j = 0
        for line in self.treeFile.read().splitlines():
            if j <= 0:
                j += 1
            else:
                tree = read_line(line)
                FID = int(tree[0])
                x = tree[1]
                y = tree[2]
                height = tree[3]
                radius = tree[4]    # at intersection
                max_radius = tree[5]
                crown_half = tree[6]

                # set max reference voxel limits
                extractTrees(x,y,max_radius, self.defInName, self.defOutName+"temp_max.las")
                self.las2txt("temp_max")
                t = LAD.LAD(self.defOutName+"temp_max.txt", self.vNum)
                if not t.points:
                    continue

                # extract pt cloud for cylindrical voxels
                extractTrees(x,y,radius, self.defOutName+"temp_max.las", self.defOutName+"temp_cyn.las")
                self.las2txt("temp_cyn")
                t.setLAD(self.defOutName+"temp_cyn.txt", 1) #0 = do not re-process file

                # cylindrical method
                lad_cyn = t.lad
                # print t.lai, sum(lad_cyn)*t.h
                # self.LAI_list.append(t.lai)
                # t.pt_lad(t.lad)

                # get LAD at each height and radius
                lad_act = [-999]*self.vNum
                print "extracting tree ", FID
                # extractTrees(x,y,radius, self.defInName, self.defOutName+"A2_"+ str(i-1) + ".las")
                for i in range(0, self.vNum):
                    rad_new = get_radius(height, max_radius, crown_half, t.heights[i])
                    rad_new = max(rad_new, 0.3)
                    extractTrees(x, y, rad_new, self.defOutName+"temp_max.las", self.defOutName+"temp_ell.las")
                    self.las2txt("temp_ell")
                    t.setLAD(self.defOutName+"temp_ell.txt", 1)
                    lad_act[i] = t.lad[i]

                # store info
                # LADs
                if FID in self.FID_list or self.FID_list == []:
                    self.LAD_list.append((FID, x, y, tree[2], t, lad_act))
                    self.LAD_cyn_list.append((FID, x, y, tree[2], t, lad_cyn))
                # LAD diff
                for i in range(0, self.vNum):
                    diff = lad_act[i] - lad_cyn[i]
                    self.LAD_diff[i].append(diff)
                lai = sum(lad_act)*t.h
                lai_cyn = sum(lad_cyn)*t.h
                self.LAI_list.append(lai)
                self.LAI_cyn_list.append(lai_cyn)

                # # skip trees
                # j -= 9

    # convert to txt
    def las2txt(self, las_file):
        FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
        args = "C:\School\\14au\Research\LAStools\LAStools\\bin\las2txt.exe -i " + \
               self.defOutName + las_file + ".las -o " + self.defOutName + las_file + ".txt -parse xyznca"
        subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)


def read_line(line):
    # print line
    t = []
    for i in line.split("\t"):
        # print i
        if i: t.append(float(i))
    # t = tuple([float(i) for i in line.split("\t")])
    # print t
    return t

# # lad shaped tree voxel
# def get_radius(height, zm, lm, z):
#     n = 0.5
#     if z <= zm:
#         n = 6
#     xx = (height-zm)/(height-z)
#     ret = 0
#     if xx > 0:
#         ret = lm*(xx**n)*math.exp(n*(1-xx))
#     else:
#         print 'heights do not match'
#     return ret

# height of tree, a, b, height of voxel
def get_radius(height, a, b, z):
    h = height - b
    xx = a**2 * (1-((z-h)/b)**2)
    if xx > 0:
        ret = math.sqrt(xx)
    else:
        ret = 0
        # print 'error in heights (height, a, b, z, xx): ', height, a, b, z, xx
    return ret


def pt_lad(self, tree, lad):
    tree.pt_lad(lad)


# extract trees
def extractTrees(x, y, radius, fin, fout):
    FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
    args = "C:\School\\14au\Research\LAStools\LAStools\\bin\lassort.exe -i " + \
           fin + " -o " + fout + " -keep_circle " + \
           str(x) + " " + str(y) + " " + str(radius)
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)


# extract trees
def viewTree(treeFile):
    FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
    args = "C:\School\\14au\Research\LAStools\LAStools\\bin\lasview.exe -i " + \
           treeFile
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)