__author__ = 'Kunxuan'

import os.path
import sys
from LAD import *
from readTrees import *
import numpy as np
import pickle

# filename = "C:\School\\14au\Research\CZOSangamonIR\las\\all_1_t4c.txt"
# # test height and z location of trees
# if not os.path.isfile(filename):
#     print("File " + filename + " does not exist")
#     sys.exit(1)
#
# # try to open file
# try:
#     print "reading csd file ", filename
#     # self.file = os.open(filename, os.O_RDONLY | os.O_NONBLOCK)
#     file = open(filename, "rb")
# except:
#     print("Could not open file")
#     sys.exit(1)
# points = []
# limits = [9999, -9999]
# for line in file:
#     pt = tuple([float(i) for i in line.split(" ")])
#     points.append(pt)
#
#     # check min/max
#     z = pt[2]
#     if z<limits[0]:
#         limits[0] = z
#     elif z>limits[1]:
#         limits[1] = z
#
# print limits

# test LAD class
# t1 = LAD.LAD(filename)
# t1.buildLists()
# t1.pt_lad()
# print t1.lai
# 4 = LW

# # test get radius
# height = 10.
# a = 1.5
# b = 3.
# z = range(0,11)
# e = [get_radius(height, a, b, y) for y in z]
# for i in e: print i

# # Allerton Park all
# lasFilename = r"C:\School\14au\Research\CZOSangamonIR\las\AllertonAll_class.las"
# treeFilename = r"C:\School\14au\Research\CZOSangamonIR\Tree_Location_Data\Ellipse\CEE550_ParameterEquation_Allertonall.txt"
# pikName = r"C:\School\14au\Research\CZOSangamonIR\data_products\AllertonAll_ell.pik"
# laiFilename = "C:\School\\14au\Research\CZOSangamonIR\data_products\AllertonAll_ell_LAI.txt"

# # Allerton 1
# lasFilename = r"C:\School\14au\Research\CZOSangamonIR\las\box_1_class.las"
# treeFilename = r"C:\School\14au\Research\CZOSangamonIR\Tree_Location_Data\Ellipse\CEE550_ParameterEquation_All1.txt"
# pikName = r"C:\School\14au\Research\CZOSangamonIR\data_products\All1_ell.pik"
# laiFilename = "C:\School\\14au\Research\CZOSangamonIR\data_products\All1_ell_LAI.txt"

# Allerton 2
lasFilename = r"C:\School\14au\Research\CZOSangamonIR\las\box_2_class.las"
treeFilename = r"C:\School\14au\Research\CZOSangamonIR\Tree_Location_Data\Ellipse\CEE550_ParameterEquation_All2.txt"
pikName = r"C:\School\14au\Research\CZOSangamonIR\data_products\All2_ell.pik"
laiFilename = "C:\School\\14au\Research\CZOSangamonIR\data_products\All2_ell_LAI.txt"

# # Home Wood
# lasFilename = r"C:\School\14au\Research\CZOSangamonIR\las\box_3_class.las"
# treeFilename = r"C:\School\14au\Research\CZOSangamonIR\Tree_Location_Data\Ellipse\CEE550_ParameterEquation_HomeWood.txt"
# pikName = r"C:\School\14au\Research\CZOSangamonIR\data_products\HOM1_ell.pik"
# laiFilename = "C:\School\\14au\Research\CZOSangamonIR\data_products\HOM1_ell_LAI.txt"


# # Lake of the Woods
# lasFilename = r"C:\School\14au\Research\CZOSangamonIR\las\box_4_class.las"
# treeFilename = r"C:\School\14au\Research\CZOSangamonIR\Tree_Location_Data\Ellipse\CEE550_ParameterEquation_LakeoftheWood.txt"
# pikName = r"C:\School\14au\Research\CZOSangamonIR\data_products\LW1_ell.pik"
# laiFilename = "C:\School\\14au\Research\CZOSangamonIR\data_products\LW1_ell_LAI.txt"

redo = 1
# FID_list = [3480, 270, 4600, 1220, 3790, 2250, 3350, 4660, 160, 1320, 4820, 0]
FID_list = []
# unpickle if available ! can't pickle file objects
if not os.path.isfile(pikName) or redo:
    print("File " + pikName + " does not exist, reading and pickling")
    r = readTrees(treeFilename, lasFilename, FID_list)
    p = [r.LAD_list, r.LAD_cyn_list, r.LAD_diff, r.LAI_list, r.LAI_cyn_list]
    # pickel object
    pickle.dump(p, open(pikName, "wb"))
else:
    print "loading from pickle"
    p = pickle.load(open(pikName, "rb"))

# check lai outfile
# if not os.path.isfile(laiFilename):
#     print("File " + laiFilename + " does not exist")
#     sys.exit(1)

# try to open file
try:
    print "opening file ", laiFilename
    # self.file = os.open(filename, os.O_RDONLY | os.O_NONBLOCK)
    laiFile = open(laiFilename, "wb")
except:
    print("Could not open file")
    sys.exit(1)

# statistics and avg LAI
LAD_list = p[0]
LAD_cyn_list = p[1]
LAD_diff = p[2]
LAI_list = p[3]
LAI_cyn_list = p[4]
for i in range(0, len(LAI_list)):
    print>>laiFile, LAI_list[i], LAI_cyn_list[i]

l = np.array(LAI_list)
lai_avg = np.average(l)
lai_std = np.std(l)

lc = np.array(LAI_cyn_list)
lai_cyn_avg = np.average(lc)
lai_cyn_std = np.std(lc)
print lai_avg, lai_std
print lai_cyn_avg, lai_cyn_std
# for l in LAD_diff:
#     print l
#
# for i in range(0, len(FID_list)):
#     tree = LAD_list[i]
#     print "FID: ", tree[0]
#     tree[4].pt_lad(tree[5])
#     # print "LAI: ", LAI_list[FID_list[i]]
#     print ""
#     # print tree[4].lai
#
# for i in range(0, len(FID_list)):
#     tree = LAD_cyn_list[i]
#     print "FID_cyn: ", tree[0]
#     tree[4].pt_lad(tree[5])
#     lai = sum(tree[5])*tree[4].h
#     # print "LAI?: ", LAI_list[FID_list[i]]
#     print ""

# # view tree
# outFilename = "C:\School\\14au\Research\CZOSangamonIR\las\Tree_Location_Data\\LW_0.las"
# viewTree(outFilename)